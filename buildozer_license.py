from subprocess import Popen, PIPE, STDOUT

p = Popen(['buildozer', 'android', 'debug', 'deploy', 'run'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
grep_stdout = p.communicate(input=b'y\n')[0]
print(grep_stdout)
