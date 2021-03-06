# -*- coding: utf-8 -*-
## Simple demo for pyffmpegb 
## 
## Copyright -- Bertrand Nouvel 2009

## import your modules

from pyffmpeg import *
from PyQt4 import QtCore
from PyQt4 import QtGui

import sys, numpy

  
try:
    LazyDisplayQt__imgconvarray={
                      1:QtGui.QImage.Format_Indexed8,
                      3:QtGui.QImage.Format_RGB888,
                      4:QtGui.QImage.Format_RGB32
                      }
except:
    LazyDisplayQt__imgconvarray={
                      1:QtGui.QImage.Format_Indexed8,
                      4:QtGui.QImage.Format_RGB32
                      }

qapp = QtGui.QApplication(sys.argv)
qapp.processEvents()


class LazyDisplayQt(QtGui.QMainWindow):
        imgconvarray=LazyDisplayQt__imgconvarray
        def __init__(self, *args):
            QtGui.QMainWindow.__init__(self, *args)
            self._i=numpy.zeros((1,1,4),dtype=numpy.uint8)
            self.i=QtGui.QImage(self._i.data,self._i.shape[1],self._i.shape[0],self.imgconvarray[self._i.shape[2]])
            self.show()
        def __del__(self):
            self.hide()
        def f(self,thearray):
            #print "ARRAY",
            #print thearray
            self._i=thearray.astype(numpy.uint8).copy('C')
            self.i=QtGui.QImage(self._i.data,self._i.shape[1],self._i.shape[0],self.imgconvarray[self._i.shape[2]])
            self.update()
            qapp.processEvents()
        def paintEvent(self, ev):
            self.p = QtGui.QPainter()
            self.p.begin(self)
            self.p.drawImage(QtCore.QRect(0,0,self.width(),self.height()),
                             self.i,
                             QtCore.QRect(0,0,self.i.width(),self.i.height()))
            self.p.end()


TS_VIDEO_RGB24={ 'video1':(0, -1, {'pixel_format':PixelFormats.RGB24})}
TS_VIDEO_BGR24={ 'video1':(0, -1, {'pixel_format':PixelFormats.BGR24})}


## create the reader object

mp=FFMpegReader()


## open an audio video file

vf=sys.argv[1]
#vf="/home/tranx/conan1.flv"
sys.stderr.write("opening\n")
mp.open(vf,TS_VIDEO_RGB24)
print "opened"
tracks=mp.get_tracks()


## connect video and audio to their respective device

ld=LazyDisplayQt()
tracks[0].set_observer(ld.f)

print "duration=",mp.duration()

#tracks[0].seek_to_seconds(10)


## play the movie !

mp.run()


