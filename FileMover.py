# -*- coding: euc-kr -*-
import os
from Tkinter import *
from tkFileDialog import askdirectory
from PIL import Image
from PIL.ExifTags import TAGS
from os import listdir, makedirs, path, access, R_OK  # W_OK for write permission.
from os.path import isfile, join, getmtime, isdir, exists
import errno
import shutil
from datetime import datetime
import time
import sys
import glob

def mkdir_p(path):
    """ 'mkdir -p' in Python """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def getDate(pullPath):
    try :
        ct = getmtime(pullPath)
        year = datetime.fromtimestamp(ct).strftime('%Y')
        month = datetime.fromtimestamp(ct).strftime('%m')
        day = datetime.fromtimestamp(ct).strftime('%d')

        return year + '/' + month + '/' + day
    except :
        return '2015/02/08'

def get_exif(filename):
    try:
        ret = {}
        i = Image.open(filename)
        info = i._getexif()
        t = info[0x9003]
        return t[0:4]+"/"+ t[5:7]+"/"+t[8:10]
    except :
        return getDate(filename)

def move(srcPath, desPath, filename):
    if exists(desPath):
        desFullPath = desPath + '/' + filename

        if exists(desFullPath):
            desPath += '/dup'
            move(srcPath, desPath, filename)
        else:
            srcPath += '/' + filename
            desPath += '/' + filename
            print srcPath + ' -> ' + desPath
            if os.path.exists(desPath) and path.isfile(desPath) and access(desPath, R_OK):
                print ("File exists and is readable")
            #This part will Check if the file exist on the server, and copy to the local machine
            elif path.exists(srcPath) and path.isfile(srcPath) and access(srcPath, R_OK) :
                try:
                    shutil.move(srcPath,desPath)
                    #os.system('move %s %s' % (srcPath, desPath))
                    del srcPath
                    del desPath
                    print ("Moviing File")
                except WindowsError as e:
                    print "WindowsError"

    else:
        mkdir_p(desPath)



def doWork(srcPath, desPath, filename) :
    tempPath = os.path.join(srcPath , filename)

    try :
        desPath = os.path.join(desPath, get_exif(tempPath) )
    except IOError as e:
        desPath =  os.path.join(desPath, getDate(tempPath))

    #print desPath
    move(srcPath, desPath, filename)

def check_condition(filename):
    return filename.upper().endswith(".JPG") \
           or filename.upper().endswith(".MOV") \
           or filename.upper().endswith(".THM") \
           or filename.upper().endswith(".NEF") \
           or filename.upper().endswith(".ZIP") \
           or filename.upper().endswith(".MP4")


def search(srcPath, desPath):
    flist = os.listdir(srcPath)
    for filename in flist:
        next = os.path.join(srcPath, filename)
        if os.path.isdir(next):
            search(next, desPath)
        else:
            if (check_condition(filename)):
                #print filename
                doWork(srcPath, desPath, filename)


if __name__ == '__main__':
    srcPath = 'Z:/Photos/temp'
    desPath = 'Z:/Photos/'

    search(srcPath, desPath)
