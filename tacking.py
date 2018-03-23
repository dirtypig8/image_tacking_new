from SimpleCV import *
from time import sleep
from os import system 
import  threading
from ptz_turn import *

def yellow_detection(img):
 yellowDist=img.hueDistance((244,215,1))
 yellowDistBin=yellowDist.binarize(25)
 img2 = yellowDistBin.dilate(2)
 img3 = img2.erode(1) 
 blobs=img3.findBlobs()
 return blobs

class C_face_data():
 def __init__(self,x,y,w,h,hat,shirt):
  self.x = x
  self.y = y
  self.w = w
  self.h = h
  self.hat = hat 
  self.shirt = shirt

if __name__ == '__main__':
 screen_w=320
 screen_h=240
 #img = Image("yellow_hat_8.jpg")
 #img= img.scale(320,240)
 display = Display(resolution=(screen_w,screen_h))
 a = 0
 while not display.isDone():
  get_photo()
  #img = Image("auto.jpg")
  img = Image("upper_test.jpg")
  img = img.scale(320,240)
  face_reaslt = []
  face_num = 0
  blobs = yellow_detection(img)
  #faces=img.findHaarFeatures('upper_body2.xml')
  faces=img.findHaarFeatures('face2.xml')
  if faces:
   for face in faces:
    #img.save("upper_test.jpg")
    img.drawText(str(face_num),face.x,face.y,fontsize=40)
    face_num+=1
    #print "Face at :" + str(face.coordinates()) 
    facelayer = DrawingLayer((img.width,img.height))
    w=face.width()
    h=face.height()
    #print "x:"+str(w)+" y:"+str(h)
    facebox_dim=(w,h)
    facebox = facelayer.centeredRectangle(face.coordinates(),facebox_dim,Color.RED)
    img.addDrawingLayer(facelayer)
    img.applyLayers()
 
    hat_left_x = face.x  - (face.width()/6) 
    hat_right_x= face.x  + (face.width()/6)
    hat_up_y= face.y  - (face.height()/2)
    hat_down_y= face.y - (face.height()/4)
 
    img.dl().circle((hat_left_x,hat_up_y),4,Color.BLUE)
    img.dl().circle((hat_right_x,hat_up_y),4,Color.BLUE)
    img.dl().circle((hat_left_x,hat_down_y),4,Color.BLUE)
    img.dl().circle((hat_right_x,hat_down_y),4,Color.BLUE)
 
    shirt_left_x = face.x  - (face.width()/3)
    shirt_right_x= face.x  + (face.width()/3)
    shirt_up_y= face.y 
    shirt_down_y= shirt_up_y + (face.height())
    if (shirt_down_y > screen_h):
     shirt_down_y = screen_h
 
    img.dl().circle((shirt_left_x,shirt_up_y),3,Color.RED)
    img.dl().circle((shirt_right_x,shirt_up_y),3,Color.RED)
    img.dl().circle((shirt_left_x,shirt_down_y),3,Color.RED)
    img.dl().circle((shirt_right_x,shirt_down_y),3,Color.RED)
    #img.save("si_upperbody_de_4.jpg")
  
    if blobs:
     for b in blobs:
      if (hat_left_x < b.x < hat_right_x) and (hat_up_y < b.y < hat_down_y):
       if (b.area() >= w*h/6):
        img.dl().circle((b.x,b.y),4,Color.BLACK,filled=True)
        blobs.image = img
        b.drawMinRect(color=Color.RED)
        find_hat = 1
        break
      else:
       find_hat = 0 
    if blobs:
     for b in blobs:
      if (shirt_left_x < b.x < shirt_right_x) and (shirt_up_y < b.y < shirt_down_y):
       if (b.area()>= w*h*3):
        img.dl().circle((b.x,b.y),4,Color.BLACK,filled=True)
        blobs.image = img
        b.drawMinRect(color=Color.RED)
        find_shirt = 1
        break
      else:
       find_shirt = 0
    face_reaslt.append(C_face_data(face.x,face.y,face.width(),face.height(),find_hat,find_shirt))
   #save_jpg 
   #img.save("home" + str(face.coordinates()) + str(a) + ".jpg")
   #a+=1
  for seq in range(len(face_reaslt)):
   print 'face seq : ', seq , ' face at : (' , face_reaslt[seq].x , ',' \
, face_reaslt[seq].y , ')  \nhat : ' , face_reaslt[seq].hat , ' shirt : ' ,face_reaslt[seq].shirt
   if (not (face_reaslt[seq].hat and face_reaslt[seq].shirt)):
    print face_reaslt[seq].hat and face_reaslt[seq].shirt 
    x_diff = face_reaslt[seq].x  - (screen_w/2)
    #y_diff = face_reaslt[seq].y + face_reaslt[seq].h - (screen_h/2)
    y_diff = face_reaslt[seq].y  - (screen_h/2)
    try:
     ctrl_x = threading.Thread(target = check_x,args=(x_diff,))
     ctrl_y = threading.Thread(target = check_y,args=(y_diff,))
     ctrl_x.start()
     ctrl_y.start()
     ctrl_x.join()
     ctrl_y.join()
     break
    except:
     print "Error: thread "
  
  img.save(display)
  print "--------------------------------"
