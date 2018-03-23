from SimpleCV import *
from time import sleep
from ptz_ctrl import * 
import sys
import threading
screen_w=320
screen_h=240
old_face_x= 0
old_face_y= 0
display = Display(resolution=(screen_w,screen_h))
a=1
while not display.isDone():
 os.system("sudo rm -r auto.jpg")
 os.system("wget -q  http://admin:admin@" + ip + "/tmpfs/auto.jpg")
 frame=Image("auto.jpg")

 frame = frame.scale(screen_w,screen_h)
 faces = frame.findHaarFeatures('face2.xml')
 if faces:
  for face in faces:
   print "Face at: " + str(face.coordinates())
   facelayer = DrawingLayer((frame.width,frame.height))
   w=face.width()
   h=face.height()
   #print "x:"+str(w)+" y:"+str(h)
   facebox_dim=(w,h)
   facebox = facelayer.centeredRectangle(face.coordinates(),facebox_dim)
   frame.addDrawingLayer(facelayer)
   frame.applyLayers()

   x_diff = face.x - screen_w / 2
   y_diff = face.y - screen_h / 2
   print "x_diff:"+ str(x_diff) +" y_diff:" + str(y_diff)
   
   print 'x_diff:' , face.x - old_face_x
   old_face_x = face.x
   print 'y_diff:' , face.y - old_face_y
   old_face_y = face.y
   
   '''
   if face.x > screen_w / 2:
    ptz_right()
   elif face.x < screen_w /2 : 
    ptz_left()
   '''
   if face.y > screen_h/2:
    try:
     ctrl_y = threading.Thread(target = ptz_down)
     ctrl_y.start()
     ctrl_y.join()
    except:
     print 'y error'
   
   if face.y < screen_h/2:
    try:
     ctrl_y = threading.Thread(target = ptz_up) 
     ctrl_y.start()
     ctrl_y.join()
    except:
     print 'y error'
  

   
 else:
  print "No faces detected."
 frame.save(display)
