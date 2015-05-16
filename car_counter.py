#!/usr/bin/python 
import time
import os
import os.path
import RPi.GPIO as GPIO
from datetime import datetime
from datetime import timedelta
import signal
import sys
import SocketServer
import sys
import socket
DEBUG = 1
PORT = 8081
SERVER = None
def GetUnique():
  try:
    global SERVER
    SERVER = SocketServer.TCPServer(("localhost", PORT), None)
  except socket.error, e:
    if DEBUG:
      print str(e)
    return False
  return True 

if not GetUnique():
  if DEBUG:
    print "something already running"
  sys.exit(1)

GPIO.setmode(GPIO.BCM)
CURRENT='/home/pi/carlog/current_log'
MAX_SENSOR_READING = 1024 # 10 bit ADC
STEADY_STATE_MIN_SENSOR_READING = 20 # steady state reading should be greater than this
#MIN_SENSOR_READING = 54 # 10 bit ADC
READINGS_AVG_COUNT = 1000
MIN_SENSOR_READING =  72 # 10 bit ADC
SLEEP_TIME_MS = 4
TOLERANCE = 5 # Change as per the sensor
reading_no = 0

# if we see reading of adc high for 250msec 
# then we can assume there is a car.
# Please reconsider when car speeds are high
#MIN_CYCLES = 3 
MIN_CYCLES = 1 

fd=None
COUNTLOG = None

def CreateFileOnDateChange():
  global COUNTLOG
  global fd
  global CURRENT
  new_log = '/home/pi/carlog/carcount%s.log' %  time.strftime("%Y_%m_%d", time.localtime())
  if new_log != COUNTLOG:
    if fd:
      fd.flush()
      fd.close()
    COUNTLOG = new_log
    fd = open(COUNTLOG, "a+")
    if os.path.isfile(CURRENT):
      os.remove(CURRENT)
    os.symlink(COUNTLOG, CURRENT)
   
CreateFileOnDateChange()
fd.write("Starting new at time:%s\n" % time.strftime("%Y_%m_%d-%H:%M:%S", time.localtime()))
def signal_handler(signal, frame):
    print ' Exiting Vehicle Counter'
    if not fd.closed:
      fd.flush()
      fd.close()
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1
        GPIO.output(cspin, True)
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
# Keep the SPICLK low, reason the Pressure sensor can't source a lot of 
# current. The 5V to 3.3V voltage divider at th analog input causes
# this. DON'T MESS WITH THE CLK IF YOU DONOT UNDERSTAND THE CIRCUIT....PLZZZZZZ

SPICLK = 22
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

adc = 0    
last_read = 0   
cycles = 0          # How many times are we seeing this reading?
vehicle_detected = False
prev_tick = datetime.now()


axle_time = 0
axle_count = 0
reading_no = 0
sensor_out_all = []
car_over = False
while True:
    CreateFileOnDateChange()
    sensor_out = readadc(adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

    reading_no = reading_no + 1
    sensor_out_all.append(sensor_out)
    if len(sensor_out_all) > READINGS_AVG_COUNT:
      sensor_out_all.sort();
      sensor_out_all = sensor_out_all[READINGS_AVG_COUNT / 10 : -READINGS_AVG_COUNT / 10]
      sensor_out_all.sort()
      avg_val = sum(sensor_out_all) / len(sensor_out_all)
      if avg_val > STEADY_STATE_MIN_SENSOR_READING and (avg_val != (MIN_SENSOR_READING - 6)):
         MIN_SENSOR_READING = avg_val + 4
         fd.write("setting steady state reading %d, car tripping point: %d\n" % (avg_val, MIN_SENSOR_READING))
      sensor_out_all = []

    if ((sensor_out > MIN_SENSOR_READING) and ((time.time() - axle_time) > 0.10)) and not car_over :
      axle_time = time.time()
      axle_count += 1
      car_over = True
      fd.write("Timestamp,AxleCount:%f,%d\n" % (time.time(),axle_count))

    if sensor_out < MIN_SENSOR_READING:
      car_over = False

    tick = datetime.now()
    if DEBUG and (reading_no % (1000/SLEEP_TIME_MS)) == 0:
        print "sensor_out:%d, axle_count:%d" % (sensor_out, axle_count)

    if  (sensor_out > MIN_SENSOR_READING - 2) or ((reading_no % (1000/SLEEP_TIME_MS)) == 0):
#    if True:
       fd.write ("#%d: time.time:%f sensor: %d  \n" % (reading_no, time.time(), sensor_out))
    if reading_no % (1000/SLEEP_TIME_MS * 3)  == 0:
       fd.flush()

    # hang out and do nothing for 4msec
    time.sleep(SLEEP_TIME_MS / 1000.0)

