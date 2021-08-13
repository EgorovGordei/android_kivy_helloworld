f = open("buildozer.spec", 'r')
s = f.read()
f.close()

s = s.replace("log_level = 1", "log_level = 2")
s = s.replace("# android.accept_sdk_license = False", "android.accept_sdk_license = True")
s = s.replace("#android.permissions = INTERNET", "android.permissions = INTERNET")
s = s.replace("requirements = python3,kivy", "requirements = python3,kivy,requests")

f = open("buildozer.spec", 'w')
f.write(s)
f.close()
