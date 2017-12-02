import os
import time
for i in range(50):
    time.sleep(2)
    os.system("python sender.py testfile.txt 500 65530")
