import subprocess


bashCmd = ["toolchain", "recipes"]
process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
output, error = process.communicate()


print("DBG:OUTPUT_ERROR:", output, error)
