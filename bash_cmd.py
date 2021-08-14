import subprocess


bashCmd = ["ls", "."]
process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
output, error = process.communicate()


print("DBG:OUTPUT_ERROR:", output, error)
