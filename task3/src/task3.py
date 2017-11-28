import os
import time
#n = 3
#p = 0.05
for i in range(50):
    time.sleep(2)
    os.system("python sender.py testfile.txt 500 65530")
