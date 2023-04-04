import time
from multiprocessing import Process, Manager
def writer(dict):
    while 1:
        dict[1] = dict[1]+1
        time.sleep(2)

def reader(dict):
    while 1:
        print(dict[1])
        time.sleep(1)

if __name__ == '__main__':
    manager = Manager() # create only 1 mgr
    d = manager.dict() # create only 1 dict
    d[1] = 0
    p0 = Process(target=writer,args=(d,)) # say to 'f', in which 'd' it should append
    p1 = Process(target=reader,args=(d,)) # say to 'f', in which 'd' it should append
    
    p0.start()
    p1.start()

    p0.join()
    p1.join()