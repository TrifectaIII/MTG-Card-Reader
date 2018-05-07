#Should install requisite packages, but is as of yet UNTESTED

import subprocess

def install(name):
    subprocess.call(['pip', 'install', name])
    
install('opencv-contrib-python')
install('urllib')
install('PyQt5')