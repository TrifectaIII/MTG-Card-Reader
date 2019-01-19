#Should install requisite packages, but is as of yet mostly UNTESTED

import subprocess

def install(name):
    subprocess.call(['pip', 'install', name])
    
pkgs = ['opencv-contrib-python','urllib','PyQt5','matplotlib']

for pkg in pkgs:
    install(pkg)