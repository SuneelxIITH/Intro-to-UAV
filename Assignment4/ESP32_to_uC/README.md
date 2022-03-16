# How to flash AVR microController with an ESP32 using WiFi ?
Here ESP32 acts as a SPI MASTER (or PROGRAMMER) and AVR μC acts as a SPI SLAVE (or TARGET) and both are connected by HSPI and ICSP (_In-Circuit Serial Programming_) ports.
### Connections
**NOTE:- Since LOGIC HIGH Voltage of ESP32 3.3V, we can do connections only to AVR board which has 3.3V. If AVR's LOGIC HIGH is 5V then we have to use _Voltage Level Shifters_ otherwise we cannot transmit data between these boards.**

| ESP 32 (or _MASTER_) | AVR (or _SLAVE_)|
|:---:|:---:|
|GPIO12|MISO|
|GPIO13|MOSI|
|GPIO14|SCK|
|GPIO5|RESET|

Reference images:-\
![alt text](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4Hr-dnKWMa2NF23e36KJhG2Oy2RwCDWpDyIc7jR5-TsRmk2DnhE-Wp0uT3tTM3YvKit4&usqp=CAU)
![alt text](https://circuits4you.com/wp-content/uploads/2018/12/ESP32-Pinout.jpg)

1. Clone this repository
2. Add your network credentials in [MASTER/src/main.cpp](https://github.com/TUdayKiranReddy/Intro-to-UAV/tree/main/ESP32_to_uC/MASTER/src/main.cpp)
3. Go to [MASTER](https://github.com/TUdayKiranReddy/Intro-to-UAV/tree/main/ESP32_to_uC/MASTER), if you already have OTA running in your ESP32
```
pio run -t upload --upload-port $ESP_IPADDRESS
```
if you don't, then connect your ESP 32 to your laptop/raspi via microUSB and then execute the following
```
pio run -t upload
```
4. Go to [SLAVE](https://github.com/TUdayKiranReddy/Intro-to-UAV/tree/main/ESP32_to_uC/SLAVE), And update the $ESP_IPADDRESS.
5. Program the AVR μC accordindly and upload the firmware
```
pio run -t upload
```
6. This can be done with _avrdude_ as well
```
avrdude -c <framework> -p <device> -P net:$ESP_ADDRESS:3000 -U flash:w:<FILE>.hex -U eeprom:w:<FILE>.epp
```

### References
1. http://ww1.microchip.com/downloads/en/appnotes/atmel-0943-in-system-programming_applicationnote_avr910.pdf
2. https://github.com/lbernstone/ESP_AVRISP
3. https://forum.arduino.cc/t/ota-programming-arduino-uno-with-esp8266-via-wifi/667201/2
4. https://arduino.stackexchange.com/questions/44702/esp8266-as-isp-program-for-atmega16
