#!/bin/env  python3.6
import  os
import  sys
import  threading
import  shlex
import  subprocess
"""1、扫描给定网段ip
    2、ping 通进行记录，不通不进行记录  format： 192.168.24.155
     3、
"""
#192.168.24.0
def ping_ip(ip):
    ip1 = ip.rsqlit('.',1)[0]
    for i in range(255):
        ips=str(ip1).join('.'+str(i))
        yield  ips
def aping_1(ips):
    cmd = "ping -n 1 "+str(ips)
    args = shlex.split(cmd)
    try:
        subprocess.check_call(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    except:
        pass

if __name__ == '__main__':
    ip=sys.argv[1]
    for ips in ping_ip(ip):
        threading.Thread()
