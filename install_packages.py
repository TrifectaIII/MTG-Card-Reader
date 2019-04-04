#Should install requisite packages, but is as of yet mostly UNTESTED

import subprocess

def install(name):
    subprocess.call(['pip', 'install', name])
    
pkgs = ['opencv-contrib-python==3.4.2.17','PyQt5']

for pkg in pkgs:
    install(pkg)