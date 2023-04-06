import os
import time
import random

vals = [0,0,0,0,0,0]

while 1:
    r = random.randint(0,5)
    vals[r] = vals[r]+1
    os.system(f"py send.py {vals[0]},{vals[1]},{vals[2]},{vals[3]},{vals[4]},{vals[5]}")
    print(vals)
    time.sleep(random.randint(1,2))