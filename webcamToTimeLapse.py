#!/usr/bin/env python3
"""Webcam image downloader and Timelapse creator"""

import argparse
import datetime
import signal
import subprocess
import sys
from time import sleep
import urllib.request

def signal_handler(sig, frame):
    print(" Interrupting download...")
    print("Initializing the creation of the timelapse video...")
    createTimeLapseVid()
    sys.exit(0)

# arguments parser:
PARSER = argparse.ArgumentParser(description="Download and merge webcam images to timelapse video.")
PARSER.add_argument("-u", metavar="URL", type=str, required=False,
                    help="url for example: -u https://pljusak.com/gardun/FI9800P_00626E815E43/snap/cam_1.jpg")
PARSER.add_argument("-s", metavar="SLEEP TIMER", type=str, required=False,
                    help="refresh time in seconds, for example: '-s 300'. If none set, 5min will be used.")
PARSER.add_argument("-c", metavar="CREATE TIMELAPSE", type=str, required=False,
                    help="usage: -c ./folderwithimages/ . Create timelapse from all images in folder. Will be also merged on interrupt CTRL-C")
PARSER.add_argument('-d', metavar='DIRECTORY', type=str, required=False,
                    help="set destination directory, default is current directory of this .py file")
PARSER.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")

def main():
    signal.signal(signal.SIGINT, signal_handler)
    args = PARSER.parse_args()

    if args.s == None:
        sec = 300

    while True:
        fileName = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M.jpg")
        urllib.request.urlretrieve(args.u, fileName)
        sleep(sec)
    
    exit()

def createTimeLapseVid():
    #TODO...
    #subprocess.run("cat *.jpg | ffmpeg -f image2pipe -i - output.mkv", shell=True, check=True)
    print("bla")
    return

if __name__ == "__main__":
    main()
