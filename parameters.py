import time
import subprocess
import numpy
import math

Y = []


def average_rssi():
    avg = 0
    for i in range(20):
        result = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
        x = result.decode('ASCII')
        y = list(x.split())

        for i in range(len(y)):
            if y[i] == 'Signal':
                a = y[(i + 2)]
                signal = a[0:len(a) - 1]

        dbm = ((int(signal)) / 2) - 100
        print(dbm)
        avg += dbm
        time.sleep(20)

    avg /= 20
    return avg


for i in range(10):
    rssi = average_rssi()
    Y.append(rssi)
    print(Y)
    time.sleep(5)

print(Y)
Y = numpy.array(Y)
Y.reshape((10,1))

Z = numpy.array([[1, -10 * math.log(1.5, 10)],
                 [1, -10 * math.log(2, 10)],
                 [1, -10 * math.log(3, 10)],
                 [1, -10 * math.log(3.5, 10)],
                 [1, -10 * math.log(4, 10)],
                 [1, -10 * math.log(4.5, 10)],
                 [1, -10 * math.log(5, 10)],
                 [1, -10 * math.log(5.5, 10)],
                 [1, -10 * math.log(6, 10)],
                 [1, -10 * math.log(6.5, 10)]])

Z_trans = Z.transpose()
A = numpy.linalg.inv(Z_trans.dot(Z))
B = Z_trans.dot(Y)
X = A.dot(B)
rss = X[0][0]
n = X[1][0]
print(rss)
print(n)
