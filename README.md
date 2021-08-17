# Wifi-Positioning-System
This project aims at getting the coordinates of a receiver in an area having 3 access points or Wifi Routers
which act as transmitters. This consists of 3 steps: Firstly getting the received signal strength in dbm by the receiver
from all the 3 transmitters, Secondly getting the distance from the 3 access points through the received signal strength from access points
using Logarithmic Distance Path Loss Model which describes the path loss by a signal as a function of distance, and lastly
calculating the coordinates of receiver if coordinates of transmitter and distance from them is known.

## Prerequisites :
The project is made using Python, so requires a knowledge of Python. Other libraries used are as follows: -
```
-> subprocess
-> numpy
-> time
-> openpyxl
-> math
```

## Theory:
The project uses subprocess library to get output of Command Prompt command 'netsh wlan show network mode=Bssid'
which gives a list of the wifi signals present near the receiver and their related information from which we can get 
the received signal strength in %. 
To convert it into dbm I used a scale of -50 dbm to -100 dbm. -50dbm represents 100% signal strength while
-100 dbm being the least received signal strength represents 0% and used linear interpolation to get received signal
strength in dbm from %.
In the next to calculate the distance from 3 access points from their corresponding signal strength
I used Logarithmic Path Loss Model which is as follows: -
```
Pl(d) = Pl(d0) + 10*n*log(d/d0) + X
where Pl(d) -> path loss at a distance d from transmitter
n -> attenuation factor
d0 -> reference distance from transmitter usually taken 1m
Pl(d0) -> path loss at distance d0 from transmitter
X -> Guassian Random Variable with zero mean describing attenuation caused by flat fading.

Pl(d) = PT - PR
where PT -> transmitted power in dbm
PR -> received power in dbm

Therfore Pr can be effectively written as
PR = Pl(d0) - 10*n*log(d/d0)
now here Pl(d0) is constant which takes care of transmitting power of transmitters, 
path loss at distance d0 and Guassian Random Variable

So distance d can be given as : -
d = d0*10^((Pl(d0)-Pl(d))/10*n)
```
Now once the distances are calculated and if we know the coordinates of the access points or the transmitters then we can calculate the coordinates 
of receiver by distance formula. In this case of 3 access points we will get 3 equations corrsponding to distances from 3 access points. These equations 
will be containing square terms so subtract the last equation from the rest two to get rid of sqaure terms and write the resulting 2 equations in the form 
matrix multiplication of the form Ax = b and use least square algorithm to get x which will give the coordinates of receiver.
