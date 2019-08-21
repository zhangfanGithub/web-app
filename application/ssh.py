import  paramiko
import  os
import  threading
import  sys
def  remote_comm(host,name,pwd,command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=host,port=22,username=name,password=pwd)
        stdin,stdout,stderr=ssh.exec_command(command)
        out=str(stdout.read(),encoding='utf-8')

        err=str(stderr.read(),encoding='utf-8')
        if out:
            print("[%s] OUT:\n%s" % (host,out))
        if err:
            print("[%s] ERROR:\n%s" % (host,err))
    except Exception as e:
        print(e)
        exit(3)

    finally:
        ssh.close()
def red_file():
    """"
    读取当前目录文件（hosts）
    ip，name，pwd
    """
    if not os.path.exists("hosts"):
        print("file hosts not find")
        exit(1)
    with open("hosts","r") as f:
        for line in f:
            if not line:
                break
            ips=line.split(',')[0]
            names=line.split(',')[1]
            pwds=line.split(',')[2].replace('\n','')
            yield  ips,names,pwds


if __name__ == '__main__':
    command=sys.argv[1]
    #command="echo11 'haha'"
    for ip,name,pwd in red_file():
        print(ip,name,pwd)
        t = threading.Thread(target=remote_comm, args=(ip, name, pwd,command))
        t.start()
