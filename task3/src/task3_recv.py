import subprocess
import os
import time
for j in range(5):
    for i in range(0.01, 0.11, 0.01):
        time.sleep(2)
        os.system("python receiver.py new_file.txt {} 65530".format(p))
