# MX5-NC-Oil-Gauge

So my inspiration was obviously the fantastic gauge kit from Rotarytronics! But as i did not want to modify my gauge cluster, I decided to try and come up with something myself :)
(the provided installation manual also gives some information about the installation process of the sensor)

I used the following hardware:

- Waveshare RP2040 1.28" LCD Touchscreen + custom 3D printed gauge pod (based on https://www.printables.com/model/538771-rp2040-lcd-128-msa)
- Bosch 0261230340 combined oil pressure and temperature sensor, you should be able to find the datasheet by searching for the partnumber
- Bosch F 02U B00 751-01 5 pin trapez connector for connecting the sensor
- 1/4" NPT to M10x1.0 thread adaptor (oil filter housing is 1/4" NPT inner thread, sensor has M10x1.0 outer thread), I got mine from speedingparts.de, but you should be able to find similar ones on aliexpress
- ADS1115 ADC for data aquisition from the sensors
- 5V to 3.3 logic level converter to get the ADCs 5V I2C signal down to the 3.3V input level of the RP2040
- 12V IN to 5V / 3.3V OUT Breadboard PSU
- Fuse tap (Mini fuse size) to get the 12V from the driverside footwell fusebox
- Prototyping pcb for the ADC, LLC, and PSU
- A few meters of 4-strand 4x0,5 mm² sensor wire

The setup is as follows: The RP2040 with the LCD sits inside the gauge pod and is connected via an about 75cm long piece of an old USB cable to the ADC/PSU box, which I placed in the driver footwell area above the fusebox. The PSU gets 12V from the driver footwell fusebox and supplies 5V to the ADC and 3.3V to the RP2040. The sensor is directly connected to the ADC box (i routed the wire through the rubber grommet of the hood release cable)
The circuitry for interfacing the sensor was a bit fiddly ... be sure to connect the thermistor via a pull-down resistor (I used 1k Ohm)

Getting the old sensor out and installing the new one was a bit tricky because of the limited space + I have large hands and only had the car on jack stands. I would definitely recommend a long 27mm socket and some extensions.
