#!/bin/bash

echo Install OpenCV 3.4.3
sudo apt install -y ./install_packages/libopencv3_3.4.6-20190415.1_armhf.deb
sudo ldconfig

echo Install picamera
sudo apt install python3-picamera

