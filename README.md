Traffic-Counter
===============
 This is a project that was done to count cars passing a point for traffic management. Cars pass over a pipe that is connected to one of the nozzles of the pressure sensor. The other nozzle is kept open. The pressure
  difference causes a voltage change and that drives the ADC. R_PI reads the ADC ouput and senses the car. 
  
 
 The design was based on a R_PI, MCP3008 and a MPX5500DP. You will also need some GPIO cable, small breadboard,  resistors, potentiometers (optional) and and a multimeter. Overall the project was < $100 .
 
  The pressure sensor datasheet is here
  http://www.freescale.com/files/sensors/doc/data_sheet/MPX5500.pdf
  
  The ADC datasheet : https://www.adafruit.com/datasheets/MCP3008.pdf
  
 
  Note, the max output of the sensor is > 3.3V so technically the sensor can damage your GPIO pins. 
  Hence, use a voltage divider,   http://en.wikipedia.org/wiki/Voltage_divider
 
  Adafruit has the ADC interfacing circuit diagram for R_PI, along with the code use it.
  
  https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/overview
  
  
  In the above code make sure you adjust the sleep intervals. I did some basic back of the envelope calculations. If a car
  travels @ 30miles/hr and you have to detect that , then assuming you have a 4mm nozzle,  calculate the amount of time 
  the car is in contact with the pipe. Make sure you don't sleep longer than that time .
  
  I tested the R_PI and GPIO code using a pot. Pots are avaialable in you local radioshack for a buck or two. Finally, the pipe I 
  used was a 4mm polyurethane pipe form the local HW sotre. Cut a sufficiently long piece and seal the other end by burning it 
  with a candle or something. Make sure its air tight by dipping the pipe in water and checking for air bubbles. 
 
  
  One of the problems I faced was, I took 3 AA batteries to power the sensor. According to the sensor datasheet that isn't enough input voltage, so I had problems getting a reliable output from the sensor. To prevent sensor output problems cut a USB cable and use the 5V supply. Else you can use a 9V to 5V converter.
  
  http://www.instructables.com/id/portable-9V-to-5V-battery/
  
  R_PI is very sensitive to amount of the current coming to the board.  Make sure you are getting 700mA at least. We had 
  a problem with one of the microUSB chargers used, make sure you use a good charger. 
  
  Note: Sensor output if proportional to pressure difference. Atmospheric pressure is 101.Kpa. Again, some rough calculations will tell you what voltage you should see when one of the car wheels goes over the pipe. 
  
  GPIO loopback on the R_PI can be tested by shorting pins 19-20 using a jumper.(check the pinout again not sure about pin nos) 
  
  Have fun......
  
