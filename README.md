Traffic-Counter
===============
 This is a project that was done to count cars passing a point. The design was based on a R_PI, ADC, I used a 
  MCP3008 and a MPX5500DP. 
 Bring Up the R_PI, im using the NOOBS.zip and Raspberian. 
 
  The pressure sensor datasheet is here
  http://www.freescale.com/files/sensors/doc/data_sheet/MPX5500.pdf
  
  The idea is the cars pass on a pipe that is connected to one of the nozzles. The other nozzle is kept open. The pressure
  difference causes a voltage change and that drives the ADC. Dat is read on the R_PI as a reading from the ADC. 
  
  Note, the max output of the sensor is > 3.3V so technically the sensor can damage your GPIO pins. 
  Hence, use a voltage divider,   http://en.wikipedia.org/wiki/Voltage_divider
  
  One of the problems I faced was I took 3 AA batteries to power sensor and that caused a problem with the output of
  the sensor. To prvent sensor output problems cut a USB cable and use the 5V supply. Else you can use a 9V to 5V converter.
  
  http://www.instructables.com/id/portable-9V-to-5V-battery/
  
  R_PI is very sensitive to amount of the current coming to the board.  Make sure you are getting 700mA at least. We had 
  a problem with one of the microUSB chargers used, make sure you use a good charger. We had issues with the network. Not
  an expert, AFAIK its in series on the board and maybe that why the problems. Need to read up to confirm.
  
  
  Adafruit has the ADC interfacing logic and the circuit diagram for the R_PI, along with the code use it.
  
  https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/overview
  
  
  In the above link make sure you adjust the sleep intervals. I did some basic back of the envelope calculations. If a car
  travels @ 30miles/hr and you have to detect that then assuming you have a 4mm nozzle calculate the amount of time 
  the car is contact with the pipe make sure the sleep interval is good to sample that .
  
  I found the potentiometer test in the above link a good way to test the digital part of the circuit. Finally, the pipe I 
  used a 4mm polyurethane pipe form the local HW sotre. Cut a sufficiently long piece and seal the other end by burning it 
  with a candle or something. Make sure its air tight by dipping the pipe in water and checking for air bubbles. 
  
  Note: Sensor output if prportional to pressure difference. Atmospheric pressure is 101.Kpa. Will share my code and 
  ckt diagram soon. 
  
  
  Have fun......
  
