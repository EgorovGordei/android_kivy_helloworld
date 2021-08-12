from subprocess import Popen, PIPE, STDOUT


# change log_level = 2
f = open("buildozer.spec", 'r')
s = f.read()
f.close()
s = s.replace("log_level = 1", "log_level = 2")
f = open("buildozer.spec", 'w')
f.write(s)
f.close()

# run buildozer via Popen to provide agreement to license
p = Popen(['buildozer', 'android', 'debug', 'deploy', 'run'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
grep_stdout = p.communicate(input=b'y\n')[0]
print(grep_stdout.decode('utf-8', 'replace'))
