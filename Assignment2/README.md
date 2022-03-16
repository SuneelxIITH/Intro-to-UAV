# Assignment 2

# Tracing a triangle 10 times

## Try1:

Assuming ideal power distribution, motors and surfaces, we get exact same outputs everytime we run same command
Just running forward and turn 120 degrees 30 times should work ideally.

But real motors, power distributuion and surfaces, there is always a deviation

## Try2:

Using MPU 6050 Gyroscope.
Here I tried to measure the yaw acceleration rate and integrate it twice to get the rotation angle, to rotate exactly.
Sensor is also real and accuracy is very less, integrating it twice is accumulation error more than the simple case.

## Try3:

Using Hmc5883l Magnetometer compass to get heading direction
With this we can just get the present heading angle/yaw relative to true earths North by declaring the usage locations Declination

## Try4:

Using a central camera on the room to look at the bot from a birds eye view.
I have created a 3D model to be printed and added on the top of the bot which will be clean.
Using OpenCV to get the orientation of the bot (https://automaticaddison.com/how-to-determine-the-orientation-of-an-object-using-opencv/)
Creating a server to keep publishing the present orientation from the central navigation system. ESP 32 will be subscribing to that angle and using that as reference to correct itself to orientent itself accordingly.

3D printing failed
