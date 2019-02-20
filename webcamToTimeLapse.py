#!/usr/bin/env python3
"""Webcam image downloader and Timelapse creator"""

import argparse
import datetime
import hashlib
import os
import pathlib
import signal
import subprocess
import sys
from time import sleep
import urllib.request

def signal_handler_int(sig, frame):
    print(" Interrupting download...")
    q = input("Do you want to merge the pictures into one video? y/n: ")
    if (q == "y"):
        q = input("Please enter destination directory: ")
        fps = input("Enter the FPS for the video (0 for default): ")
        print("Initializing the creation of the timelapse video...")
        createTimeLapseVid(None, q, fps)
    else:
        print("exiting...")
    sys.exit(0)

def signal_handler_term(sig, frame):
    sys.exit(0)

# arguments parser:
PARSER = argparse.ArgumentParser(description="Download and merge webcam images to timelapse video.")
PARSER.add_argument("-u", metavar="URL", type=str, required=False,
                    help="url for example: -u https://pljusak.com/gardun/FI9800P_00626E815E43/snap/cam_1.jpg")
PARSER.add_argument("-s", metavar="SLEEP TIMER", type=str, required=False,
                    help="refresh time in seconds, for example: '-s 30'. If none set, 5min will be used. Min: 3sec, max: 600sec")
PARSER.add_argument("-f", metavar="FPS", type=str, required=False,
                    help="how many fps for the output video, for example: '-f 25'. If none set, fps will be 10. Min: 1, max: 60")
PARSER.add_argument("-c", metavar="CREATE", type=str, required=False,
                    help="usage: -c ./folderwithimages/ . Create timelapse from all images in folder. Will be also merged on interrupt CTRL-C")
PARSER.add_argument('-d', metavar='DIRECTORY', type=str, required=False,
                    help="set destination directory, default is current directory of this .py file")
PARSER.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")

def main():
    signal.signal(signal.SIGINT, signal_handler_int)
    signal.signal(signal.SIGTERM, signal_handler_term)
    args = PARSER.parse_args()

    if args.c == None and args.u == None:
        print("No arguments provided. Please use at least '-u URL' or '-c DIR'")
        exit()

    if args.c is not None:
        if args.f == None:
            createTimeLapseVid(args.c, args.d, 12)
        else:
            createTimeLapseVid(args.c, args.d, int(args.f))
        exit()

    if args.s == None or int(args.s) < 3 or int(args.s) > 600:
        sec = 300
    else:
        sec = int(args.s)

    if args.d == None:
        args.d = ""
    else:
        pathlib.Path(args.d).mkdir(parents=True, exist_ok=True)

    while True:
        fileName = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S.jpg")
        newFile = os.path.join(args.d, fileName)
        try:
            urllib.request.urlretrieve(args.u, newFile)
        except:
            print("Error while retreiving URL. Next try in ", sec," seconds.")
        sleep(sec)
    
    exit()

def createTimeLapseVid(srcDir, destDir, fps):
    if srcDir == None and destDir == None:
        srcDir = ""
        destDir = ""
    elif destDir == None:
        destDir = ""
    else:
        pathlib.Path(destDir).mkdir(parents=True, exist_ok=True)

    if fps < 1 or fps > 60:
        framerate = "-framerate 10"
    else:
        framerate = "-framerate " + str(fps)

    ffmpegRun = "cat " + srcDir + "*.jpg | ffmpeg " + framerate + " -f image2pipe -i - " + destDir + datetime.datetime.now().strftime("%Y_%m_%d.mkv")
    print("starting ffmpeg, please wait. Can take minutes, depending on hardware and amount of images...")
    print("If it takes too long, run this command and see the output of ffmpeg:")
    print(ffmpegRun)
    subprocess.run(ffmpegRun, shell=True, check=True)
    print("ffmpeg finished.")
    return

if __name__ == "__main__":
    main()
