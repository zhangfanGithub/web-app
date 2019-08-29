import  os
import  sys
import  threading
import  shlex
import  subprocess
"""1、扫描给定网段ip
    2、ping通记录，不通不记录  format： 192.168.24.155
     3、
"""
#192.168.24.0
def ping_ip(ip):
    ip1 = ip.rsplit('.',1)[0]
    for i in range(254):
        ips=str(ip1)+'.'+str(i)
        yield  ips
def aping(ips):
    cmd = "ping -n 1 "+str(ips)
    args = shlex.split(cmd)
    try:

        subprocess.check_call(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print(str(ips)+"\tok")
    except:
        exit(0)
if __name__ == '__main__':
    ip=sys.argv[1]
    for ips in ping_ip(ip):
        t=threading.Thread(target=aping, args=(str(ips),))
        t.start()
