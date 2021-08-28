f = open("buildozer.spec", 'r')
s = f.read()
f.close()

s = s.replace("log_level = 1", "log_level = 2")
s = s.replace("# android.accept_sdk_license = False", "android.accept_sdk_license = True")
s = s.replace("#android.permissions = INTERNET", "android.permissions = INTERNET,CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,RECORD_AUDIO,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION")
s = s.replace("requirements = python3,kivy", "requirements = plyer,libffi,imutils,opencv,numpy,cffi,python3==3.7.9,hostpython3==3.7.9,kivy==master,kivymd==0.104.2,sdl2_ttf==2.0.15,pillow,requests,urllib3,charset-normalizer,idna,moviepy,youtube-dl,imageio,proglog")
s = s.replace("#p4a.branch = master", "p4a.branch = develop")
s = s.replace("osx.python_version = 3", "osx.python_version = 3.7.9")

s = s.replace("#android.api = 27", "android.api = 30")

f = open("buildozer.spec", 'w')
f.write(s)
f.close()
