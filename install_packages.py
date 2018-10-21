#Should install requisite packages, but is as of yet UNTESTED

import subprocess

def install(name):
    subprocess.call(['pip', 'install', name])
    
pkgs = ['opencv-contrib-python','urllib','PyQt5']

for pkg in pkgs:
    install(pkg)