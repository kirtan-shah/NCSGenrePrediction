import os
import subprocess
import tqdm

dirpath = "../NCSDownload/songs"
files = [os.path.join(dirpath, f) for f in os.listdir(dirpath)]

durations = []

for file in tqdm.tqdm(files):
    args=("ffprobe","-show_entries", "format=duration","-i", file)
    popen = subprocess.Popen(args, stdout = subprocess.PIPE, stderr=subprocess.DEVNULL)
    popen.wait()
    output = popen.stdout.read()
    try:
        duration = output.decode("utf-8").split("=")[1].split("\n")[0]
        durations.append(float(duration))
    except:
        pass

print("Average duration: " + str(sum(durations)/len(durations)))
print("Max duration: " + str(max(durations)))
print("Min duration: " + str(min(durations)))