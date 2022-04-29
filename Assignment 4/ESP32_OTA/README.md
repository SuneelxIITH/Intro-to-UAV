# Flash firmware to ESP32 using OTA Programming 
1. Go to *OTA_code* project and add your network credentials in *src/main.cpp*.
2. Build and upload the *OTA_code* firmware via micro-USB cable.
3. Use the below command to find out the IP ADDRESS of ESP32.(*Do this while ESP32 is OFF and also after it is ON to discover new IP ADDRESS in the scan*)
```
nmap -sP <LAPTOP/PHONE_IP_ADDRESS>/24
```
4. Go to *blink* project, build and upload the firmware using the below command wirelessly.
```
pio run -t upload --upload-port $ESP32_IP
```
