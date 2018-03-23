from SimpleCV import *
from time import sleep
from os import system 
import  threading
from ptz_turn import *
from multiprocessing import Queue



def upper_detection(img,upper_q):
 l=img.findHaarFeatures('upper_body2.xml') 
 upper_q.put(l)

def face_detection(img,face_q):
 l=img.findHaarFeatures('face2.xml')
 face_q.put(l)

def upper_check(img,uppers,blobs):
 global face_result
 global face_num
 if uppers:
  for upper in uppers:
   #img.save("upper_test.jpg")
   img.drawText(str(face_num),upper.x,upper.y,fontsize=40)
   face_num+=1
   #print "Face at :" + str(face.coordinates()) 
   facelayer = DrawingLayer((img.width,img.height))
   w=upper.width()
   h=upper.height()
   #print "x:"+str(w)+" y:"+str(h)
   upperbox_dim=(w,h)
   upperbox = facelayer.centeredRectangle(upper.coordinates(),upperbox_dim,Color.RED)
   img.addDrawingLayer(facelayer)
   img.applyLayers()
   img.drawText('upper',upper.x  - (upper.width()/2),upper.y  - (upper.height()/2)-15,Color.RED,fontsize=20)
   hat_left_x = upper.x  - (upper.width()/6) 
   hat_right_x= upper.x  + (upper.width()/6)
   hat_up_y= upper.y  - (upper.height()/2)
   hat_down_y= upper.y - (upper.height()/4)
 
   img.dl().circle((hat_left_x,hat_up_y),4,Color.BLUE)
   img.dl().circle((hat_right_x,hat_up_y),4,Color.BLUE)
   img.dl().circle((hat_left_x,hat_down_y),4,Color.BLUE)
   img.dl().circle((hat_right_x,hat_down_y),4,Color.BLUE)
   
   shirt_left_x = upper.x  - (upper.width()/3)
   shirt_right_x= upper.x  + (upper.width()/3)
   shirt_up_y= upper.y 
   shirt_down_y= shirt_up_y + (upper.height())
   if (shirt_down_y > screen_h):
    shirt_down_y = screen_h

   img.dl().circle((shirt_left_x,shirt_up_y),3,Color.RED)
   img.dl().circle((shirt_right_x,shirt_up_y),3,Color.RED)
   img.dl().circle((shirt_left_x,shirt_down_y),3,Color.RED)
   img.dl().circle((shirt_right_x,shirt_down_y),3,Color.RED)
   #img.save("si_upperbody_de_4.jpg")
   w= hat_right_x - hat_left_x 
   h= hat_down_y - hat_up_y
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
   face_result.append(C_face_data(1,upper.x,upper.y,upper.width(),upper.height(),find_hat,find_shirt))

def face_check(img,faces,blobs):
 global face_result
 global face_num
 if faces:
  for face in faces:
   img.drawText(str(face_num),face.x,face.y,fontsize=40)
   face_num+=1
   #print "Face at :" + str(face.coordinates()) 
   facelayer = DrawingLayer((img.width,img.height))
   w=face.width()
   h=face.height()
   #print "x:"+str(w)+" y:"+str(h)
   facebox_dim=(w,h)
   facebox = facelayer.centeredRectangle(face.coordinates(),facebox_dim)
   img.addDrawingLayer(facelayer)
   img.applyLayers()
   img.drawText('face',face.x  - (face.width()/2),face.y  - (face.height()/2)-15,Color.ORANGE,fontsize=20)
   hat_left_x = face.x  - (face.width()/2) 
   hat_right_x= face.x  + (face.width()/2)
   hat_up_y= face.y  - (face.height())
   hat_down_y= face.y

   img.dl().circle((hat_left_x,hat_up_y),4,Color.BLUE)
   img.dl().circle((hat_right_x,hat_up_y),4,Color.BLUE)
   img.dl().circle((hat_left_x,hat_down_y),4,Color.BLUE)
   img.dl().circle((hat_right_x,hat_down_y),4,Color.BLUE)

   shirt_left_x = face.x  - (face.width())
   shirt_right_x= face.x  + (face.width())
   shirt_up_y= face.y + (face.height()/2)
   shirt_down_y= shirt_up_y + (face.height()*3)

   img.dl().circle((shirt_left_x,shirt_up_y),3,Color.RED) 
   img.dl().circle((shirt_right_x,shirt_up_y),3,Color.RED)
   img.dl().circle((shirt_left_x,shirt_down_y),3,Color.RED)
   img.dl().circle((shirt_right_x,shirt_down_y),3,Color.RED)

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
   face_result.append(C_face_data(0,face.x,face.y,face.width(),face.height(),find_hat,find_shirt))

def yellow_detection(img):
 yellowDist=img.hueDistance((244,215,1))
 yellowDistBin=yellowDist.binarize(10)
 img2 = yellowDistBin.dilate(2)
 img3 = img2.erode(1) 
 blobs=img3.findBlobs()
 #img3.show()
 return blobs

class C_face_data():
 def __init__(self,type,x,y,w,h,hat,shirt):
  self.type = type
  self.x = x
  self.y = y
  self.w = w
  self.h = h
  self.hat = hat 
  self.shirt = shirt

if __name__ == '__main__':
 #320*240 640*480 1280*720 1920*1080
 #screen_w=1920
 #screen_h=1080
 #img = Image("yellow_hat_8.jpg")
 #img= img.scale(320,240)
 display = Display(resolution=(screen_w,screen_h))
 a = 0
 while not display.isDone():
  get_photo()
  img = Image("auto.jpg")
  #img = Image("upper_test.jpg")
  #img = Image("upper_1.jpg")
  #img  = Image("../yellow_hat_8.jpg")
  img = img.scale(screen_w,screen_h)
  censor_result = []
  face_result = []
  face_num = 0
  blobs = yellow_detection(img)

  #uppers=img.findHaarFeatures('upper_body2.xml')
  #faces=img.findHaarFeatures('face2.xml')
  upper_q= Queue()
  face_q=Queue()
  try:
   t1=threading.Thread(target=upper_detection,args=(img,upper_q))
   t2=threading.Thread(target=face_detection,args=(img,face_q))
   t1.start()
   t2.start()
   t1.join()
   t2.join()
   faces=face_q.get()
   uppers=upper_q.get()
  except:
   print "face or upper error"

  print 'uppers : ', uppers
  print 'faces : ' , faces
  if uppers:
   for upper in uppers:
    if faces:
     for face in faces:
      upper_left_x = upper.x - upper.width()/2
      upper_right_x = upper.x + upper.width()/2     
      upper_up_y = upper.y - upper.height()/2
      upper_down_y = upper.y + upper.height()/2
      if (upper_left_x < face.x < upper_right_x) and ( upper_up_y < face.y < upper_down_y):
       uppers.remove(upper)
       break
  
  print 're_uppers : ', uppers
  print 're_faces : ' , faces
 
  try:
   check_1=threading.Thread(target = upper_check,args=(img,uppers,blobs))
   check_2=threading.Thread(target = face_check,args=(img,faces,blobs))
   check_1.start()
   check_2.start()
   check_1.join()
   check_2.join()
   #face_check(img,faces,blobs)
  except:
   print 'check_error'
  print 'result',len(face_result)
  for seq in range(len(face_result)):
   print 'seq : ', seq ,'face 0 or upper 1 : ',face_result[seq].type,  ' upper at : (' , face_result[seq].x , ',' \
, face_result[seq].y , ')  \nhat : ' , face_result[seq].hat , ' shirt : ' ,face_result[seq].shirt , '...'


  for seq in range(len(face_result)):
   if (not (face_result[seq].hat and face_result[seq].shirt)):
    if (face_result[seq].type == 1): 
     #print face_result[seq].hat and face_result[seq].shirt 
     x_diff = face_result[seq].x  - (screen_w/2)
     y_diff = face_result[seq].y + face_result[seq].h - (screen_h/2)
     y_diff = face_result[seq].y  - (screen_h/2)
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

    elif (face_result[seq].type == 0):
     x_diff = face_result[seq].x  - (screen_w/2)
     y_diff = face_result[seq].y + face_result[seq].h - (screen_h/2)
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
  '''
  if faces or uppers:
   #save_jpg 
   img.save("tku_home" + str(a) + ".jpg")
   a+=1
   if a==25 : 
    break
  '''
  img.save(display)
  
  print "--------------------------------"
