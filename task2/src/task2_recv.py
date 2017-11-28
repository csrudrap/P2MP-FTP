import subprocess
while True:
    out = subprocess.check_output("ps -ef | grep receiver.py", shell=True)
    if len(out.split('\n')) == 3:
        os.system("python receiver.py new_file.txt 0.05 65530")
