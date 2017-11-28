import os
import time
n = 3
p = 0.05
for i in range(5):
    for j in range(100, 1000, 100):
        time.sleep(0.5)
        os.system("python sender.py testfile.txt {} 65530".format(j))
