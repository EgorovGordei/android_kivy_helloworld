f = open("buildozer.spec", 'r')
s = f.read()
f.close()

s = s.replace("log_level = 1", "log_level = 2")
s = s.replace("# android.accept_sdk_license = False", "android.accept_sdk_license = True")
s = s.replace("#android.permissions = INTERNET", "android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION")
s = s.replace("requirements = python3,kivy", "requirements = libffi,cffi,python3,kivy==master,kivymd==0.104.2,sdl2_ttf==2.0.15,pillow,requests,urllib3,charset-normalizer,idna,plyer")
s = s.replace("#p4a.branch = master", "p4a.branch = develop")

f = open("buildozer.spec", 'w')
f.write(s)
f.close()
