#!/bin/bash

echo Install OpenCV 3.4.6
#sudo apt install -y ./install_packages/libopencv3_3.4.6-20190415.1_armhf.deb
#sudo ldconfig
sudo pip3 install opencv_python
sudo apt install libjasper1 libcblas-dev libatlas3-base

echo Install picamera
sudo apt install python3-picamera
