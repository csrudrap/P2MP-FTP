import subprocess
import os
import time
for j in range(5):
    for i in range(1, 11, 1):
        time.sleep(2)
        os.system("python receiver.py new_file.txt {} 65530".format(float(p)/100))
