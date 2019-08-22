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
        print("出错了：",e)
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

def  sftp_client(host,name,pwd):
    transport = paramiko.Transport((host, 22))
    transport.connect(username=name, password=pwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return  sftp

def up_file(host,name,pwd,loadfile,remotefile):
    sftp=sftp_client(host,name,pwd)
    sftp.put(loadfile,remotefile)
    print("上传成功")
    sftp.close()
def down_file(host,name,pwd,remotefile,loadfile):
    sftp = sftp_client(host, name, pwd)
    sftp.get(remotefile,loadfile)
    print("下载成功")
    sftp.close()
def exist_file_load_put(file):
    if not os.path.exists(file):
        print("upload file not find")
        exit(5)
    return file
def exist_file_load_down(file):
    if  os.path.exists(file):
        print("down file already exist")
        exit(6)
    return file

if __name__ == '__main__':
    option=sys.argv[1]
    #option="-put"
    if option=="--help":
        print("option\n\t-m\teg:\tssh.py\t-m\t'echo hello'\t\t\t\t\t#command shell\n "
              "\t-put\teg:\tssh.py\t-put\tD:\HELLO\host\t/root/host(需要带文件名)\t#上传文件\n"
              "\t-down\teg:\tssh.py\t-down\t/tmp/hosts\tD:/HELLO/hosts(需要带文件名)\t#下载文件\n")
    elif option=="-m":
        command = sys.argv[2]
        for ip, name, pwd in red_file():
            print(ip, name, pwd)
            t = threading.Thread(target=remote_comm, args=(ip, name, pwd, command))
            t.start()
    elif option=="-put":
        """put file"""

        load = r''+exist_file_load_put(sys.argv[2])
        remote = sys.argv[3]
        #load = r"D:\python_project\web-app\web-app\application\hosts"
        #remote = "/root/hosts"
        for ip, name, pwd in red_file():
            print(ip, name, pwd)
            t = threading.Thread(target=up_file, args=(ip, name, pwd,load,remote))
            t.start()
    elif option=="-down":
        """down file"""
        remote = r''+sys.argv[2]
        load = r''+exist_file_load_down(sys.argv[3])
        for ip, name, pwd in red_file():
            print(ip, name, pwd)
            t = threading.Thread(target=down_file, args=(ip, name, pwd, remote,load))
            t.start()