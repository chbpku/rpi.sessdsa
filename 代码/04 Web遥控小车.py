import cherrypy
import os
from cherrypy.lib.static import serve_file
import RPi.GPIO as GPIO
import time

base_dir = os.path.dirname(os.path.realpath(__file__))

class CAR:
  IN1 = 11
  IN2 = 12
  IN3 = 13
  IN4 = 15
  PIN1 = 31
  PIN2 = 32
  PIN3 = 33
  PIN4 = 35
  PIN5 = 36
  PIN6 = 37
  PIN7 = 38
  PIN8 = 40
  Trig = 3
  Echo = 5
  BUZZ_NO = 16
  power = 'off'

  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def change_status(self):
    if self.power == 'off':
      self.power = 'on'
      self.normal_sign()
    else:
      self.power = 'off'
      GPIO.cleanup()
    return self.power

  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def init_engine(self):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.IN1, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(self.IN2, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(self.IN3, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(self.IN4, GPIO.OUT, initial = GPIO.LOW)

  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def init_radar(self):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.Trig, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(self.Echo, GPIO.IN)

  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def init_buzzer(self):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.BUZZ_NO, GPIO.OUT, initial = GPIO.LOW)

  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def init_led(self):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.PIN1, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(self.PIN2, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(self.PIN3, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(self.PIN4, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(self.PIN5, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(self.PIN6, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(self.PIN7, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(self.PIN8, GPIO.OUT, initial = GPIO.LOW)
    
  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def forward(self):
      self.init_engine()
      GPIO.output(self.IN1, GPIO.HIGH)
      GPIO.output(self.IN2, GPIO.LOW)
      GPIO.output(self.IN3, GPIO.HIGH)
      GPIO.output(self.IN4, GPIO.LOW)

  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def left(self): 
      self.init_engine()
      GPIO.output(self.IN3, GPIO.HIGH)
      GPIO.output(self.IN4, GPIO.LOW)

  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def right(self):
      self.init_engine()
      GPIO.output(self.IN1, GPIO.HIGH)
      GPIO.output(self.IN2, GPIO.LOW)

  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def backward(self):
      self.init_engine()
      GPIO.output(self.IN1, GPIO.LOW)
      GPIO.output(self.IN2, GPIO.HIGH)
      GPIO.output(self.IN3, GPIO.LOW)
      GPIO.output(self.IN4, GPIO.HIGH)

  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def buzzer(self):
    self.init_buzzer()
    GPIO.output(self.BUZZ_NO, GPIO.HIGH)

  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def debuzzer(self):
    self.init_buzzer()
    GPIO.output(self.BUZZ_NO, GPIO.LOW)
    
  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def check_distance(self):
    self.init_radar()
    GPIO.output(self.Trig, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(self.Trig, GPIO.LOW)
    while not GPIO.input(self.Echo):
            pass
    t1 = time.time()
    while GPIO.input(self.Echo):
            pass
    t2 = time.time()
    result = (t2-t1)*340/2
    print(result)
    return {'distance':'%.3f' % result, 'unit':' m'}
  
  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def normal_sign(self):
          self.init_led()
          GPIO.output(self.PIN1, GPIO.HIGH)
          GPIO.output(self.PIN6, GPIO.HIGH)
          GPIO.output(self.PIN8, GPIO.HIGH)

  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def normal_sign2(self):
          self.init_led()
          GPIO.output(self.PIN4, GPIO.HIGH)
          GPIO.output(self.PIN7, GPIO.HIGH)

  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def normal_sign3(self):
          self.init_led()
          GPIO.output(self.PIN2, GPIO.HIGH)
          GPIO.output(self.PIN5, GPIO.HIGH)
          GPIO.output(self.PIN3, GPIO.HIGH)

  @cherrypy.expose()
  @cherrypy.tools.json_out()
  def all_sign(self):
          self.init_led()
          GPIO.output(self.PIN1, GPIO.HIGH)
          GPIO.output(self.PIN2, GPIO.HIGH)
          GPIO.output(self.PIN3, GPIO.HIGH)
          GPIO.output(self.PIN4, GPIO.HIGH)
          GPIO.output(self.PIN5, GPIO.HIGH)
          GPIO.output(self.PIN6, GPIO.HIGH)
          GPIO.output(self.PIN7, GPIO.HIGH)
          GPIO.output(self.PIN8, GPIO.HIGH)
          
cherrypy.server.socket_host = '0.0.0.0'

conf = {
  '/': {
    'tools.sessions.on':True,
    'tools.staticfile.on': True,
    #'tools.staticdir.root':os.path.abspath("/home/pi/"),
    'tools.staticfile.filename': base_dir + '/FINAL WORK.html'
    
  },
  '/static':{
    'tools.staticdir.on':True,
    'tools.staticdir.dir': base_dir
  }
        
  
}

cherrypy.quickstart(CAR(), '/', conf)
