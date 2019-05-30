## UPDATE (5/29/2019)
### V2.0
I am happy to report that [v2.0 of MTG-Card-Reader](https://github.com/TrifectaIII/MTG-Card-Reader-Web), a web-based in-browser version is in active development. If you have any interest in contributing to development of v2.0, send me an e-mail at maddenfong@gmail.com. I am a complete novice regarding web hosting/web deployment of a project like this and could use some help.
### A note on this version
At the moment, this original version of the project is experiencing some major crashing issues (at least on my machine) but they are not throwing error messages and I'm too busy with v2.0 to hunt them down, sorry ☹️. I recently swapped the feature description algorithm from SIFT to ORB (which means any semi-recent version of opencv-python is good, don't need specific versions of -contrib anymore) but the crashes were happening before that.

# MTG-Card-Reader

Reads a Magic: The Gathering card in front of a webcam and identifies it in an existing database of cards of a user-specified set.

[__See it in action here!__](https://www.youtube.com/watch?v=KvsBkOgKNgQ)

<a href="http://www.youtube.com/watch?feature=player_embedded&v=KvsBkOgKNgQ
" target="_blank"><img src="http://img.youtube.com/vi/KvsBkOgKNgQ/0.jpg" 
width="240" height="180" border="10" /></a>

Download the Allset.json file (zipped or unzipped) from the MTGJSON website listed below, and place in project folder. Then run __MTGCardReader.py__ to start the program.

When loading up a set for the first time, the program may take 5 minutes or more to download and store all images from that set.

Run __install_packages.py__ to install the requisite packages _(NOTE: This is mostly untested)_

Open __Thesis Paper - MTG Card Reader.pdf__ to read about this project in more detail.

## Resources
Uses MTGJSON, Python 3, Qt5, PyQt5, OpenCV, URLLib

https://mtgjson.com/

https://www.python.org/

https://www.riverbankcomputing.com/software/pyqt/download5

https://pypi.org/project/opencv-python/

https://docs.python.org/3/library/urllib.html

## About Me

I am a recent university grad currently living and looking for a job in San Francisco. If you would like to contact me about this software project (or anything else) please send an email to maddenfong@gmail.com
