from ptz_ctrl_2 import *
from math import ceil
def get_photo():
 system("sudo rm -r auto.jpg")
 system("wget -q  http://admin:admin@" + ip + "/tmpfs/auto.jpg")

screen_w=320
screen_h=240

#ptz_ctrl
# 320*240 x:13 y:15


#ptz_ctrl_2
#320*240   x:65 y:50
#640*480   x:128 y:100
#1280*720  x:199 y:169
#1920*1080 x:280 y:228
def check_x(x_diff):
 
 min_x = 65
 if x_diff >= ceil(min_x/2.0):
  x_count = x_diff / min_x
  if x_diff % min_x >= ceil(min_x/2.0):
   x_count+=1
  for count in range(0,x_count,1):
   ptz_right()

 elif x_diff <= -ceil(min_x/2.0) :
  x_count = abs(x_diff) / min_x
  if abs(x_diff) % min_x >= ceil(min_x/2.0):
   x_count+=1
  for count in range(0,x_count,1):
   ptz_left()

def check_y(y_diff):
 min_y = 50
 if y_diff >= ceil(min_y/2.0):
  y_count = y_diff / min_y
  if y_diff % min_y >= ceil(min_y/2.0):
   y_count+=1
  for count in range(0,y_count,1):
   ptz_down()

 elif y_diff <= -ceil(min_y/2.0):
  y_count = abs(y_diff) / min_y
  if abs(y_diff) % min_y >= ceil(min_y/2.0):
   y_count+=1
  for count in range(0,y_count,1):
   ptz_up()

