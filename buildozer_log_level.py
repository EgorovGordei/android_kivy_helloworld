# change log_level = 2
f = open("buildozer.spec", 'r')
s = f.read()
f.close()
s = s.replace("log_level = 1", "log_level = 2")
f = open("buildozer.spec", 'w')
f.write(s)
f.close()
