import subprocess


bashCmd = ["toolchain", "recipes"]
process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
output, error = process.communicate()

output = output.decode(errors="ignore")

counter = 0
new_output = ""
for letter in output:
    if counter == 0 and letter == " ":
        counter = 1
        new_output += " "
    elif counter == 1 and letter == "\n":
        counter = 0
    elif counter == 0:
        new_output += letter
output = new_output

bashCmd = ["toolchain", "build", "python3"] + list(output.split(" "))
print("Recipes\n:", bashCmd)
process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
output, error = process.communicate()
