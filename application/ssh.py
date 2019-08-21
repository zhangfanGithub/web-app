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
def up_file(host,name,pwd,loadfile,remotefile):
    transport=paramiko.Transport((host,22))
    transport.connect(username=name,password=pwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(loadfile,remotefile)
    print("上传成功")
    transport.close()
def exist_file(file):
    if not os.path.exists(file):
        print("file not find")
        exit(5)
    return file
if __name__ == '__main__':
    option=sys.argv[1]

    #command="echo11 'haha'"

    if option=="--help":
        print("option  -m   eg: ssh.py  -m  'echo hello' "
              " -put  eg:ssh.py  -put load.txt  remote.txt"
              " -down eg:ssh.py -down  /tmp/hosts  loaddir")

    elif option=="-m":
        command = sys.argv[2]
        for ip, name, pwd in red_file():
            print(ip, name, pwd)
            t = threading.Thread(target=remote_comm, args=(ip, name, pwd, command))
            t.start()
    elif option=="-put":
        """put file"""
        load = exist_file(sys.argv[2])
        remote = sys.argv[3]
        for ip, name, pwd in red_file():
            print(ip, name, pwd)
            t = threading.Thread(target=up_file, args=(ip, name, pwd,load,remote))
            t.start()