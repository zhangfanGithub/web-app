from  multiprocessing  import  Pool
import  os,time

def task(id):
    print("child  process %s  start parent process %s " %  (id,os.getppid()))
    start=time.time()
    time.sleep(3)
    end=time.time()
    print("child  process %s run  %.2f time" % (id,end-start))
if __name__ == '__main__':
    print("this is main process %s" % os.getpid())
    p=Pool(4)
    for i in  range(6):
        p.apply_async(task,args=(i,))
    print('Waiting for all subprocesses.........')
    p.close()
    p.join()
    print('All subprocesses successful.')

