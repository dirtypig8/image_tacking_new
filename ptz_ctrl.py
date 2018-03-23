from os import system  
from time import sleep
ip = "192.168.0.87:6611" 
url ='curl -s -o /dev/null "http://admin:admin@' + ip + '/web/cgi-bin/hi3510/ptzctrl.cgi?-step=0&-act=' 
#320*240 640*480 1280*720 1920*1080
screen_w=320
screen_h=240
delay = .0001
def ptz_right():
 system( url + 'right"')
 sleep(delay)
 system( url + 'stop"')

def ptz_left():
 system( url + 'left"')
 sleep(delay)
 system( url + 'stop"')

def ptz_up():
 system( url + 'up"')
 sleep(delay)
 system( url + 'stop"')

def ptz_down():
 system( url + 'down"')
 sleep(delay)
 system( url + 'stop"')


if __name__ == '__main__':
 #ptz_right()  
 #ptz_left()
 ptz_up()
 #ptz_down()
