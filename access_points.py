#importing libraries needed
import subprocess
import numpy

#defining empty lists to append desired values
signal = []  #for storing signal strength percentage
signal_strength = [] #for storing signal strengths in dbm
distances = [] #for storing the distances from different access points
ssids = [] #for storing the names of hotspots
s2 = [] #for storing the index of word Network in list y
s1= [] #for storing the index of word SSID in list y

#function to get the signal strength values and converting them into 'dbm'
def signalStrength():
    #getting the result of the command of coomand prompt and storing it in a variable
    result = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])

    #converting the result(datatype = bytes) first into string object and storing each individual substring in a list y
    y = list((result.decode('ASCII')).split())

    #getting all the indexes of words SSID and Network and storing them in lists s1 and s2
    s1 = [i for i,x in enumerate(y) if x == 'SSID']
    s2 = [i for i,x in enumerate(y) if x == 'Network']

    #joining individual substrings to get one string for corresponding names of hotspots
    for i in range(len(s1)):
        c = y[(s1[i]+3):s2[i]]
        c = tuple(c)
        d = " "
        ssids.append(d.join(c))
    print(ssids)

    #getting the signal strength percentage value by removing the % sign from the string
    for i in range(len(y)):
        if y[i] == 'Signal':
            a = y[(i+2)]
            b = a[0:len(a)-1]
            signal.append(b)

    print(signal)

    #converting signal strength percentage into dbm
    for i in range(len(signal)):
        dbm = ((int(signal[i]))/2) - 100
        signal_strength.append(dbm)

    print(signal_strength)
    return signal_strength

#function to get distance from access point
#ss = signal strength due to access point at a particular point
#rss = reference signal strength at reference distance from access point
#n = signal attenuation factor
#rd = reference distance
def calc_distance(ss, rss, n, rd):
    distance = rd*(10**((rss-ss)/(10*n)))
    return distance

#function to get the coordinates of point
#parameters = position of access points and distances from those access points
def coordinates(x1, y1, x2, y2, x3, y3,  distances):
    A = numpy.array([[(2*(x1-x3)), (2*(y1-y3))], [(2*(x2-x3)), (2*(y2-y3))]], dtype=float)
    B = numpy.array([[x1*x1 + y1*y1 - x3*x3 - y3*y3 - distances[0]*distances[0] - distances[2]*distances[2]],
                     [x2*x2 + y2*y2 - x3*x3 - y3*y3 - distances[1]*distances[1] - distances[2]*distances[2]]], dtype=float)
    A_transp = A.transpose()
    C = numpy.linalg.inv(A_transp.dot(A))
    D = A_transp.dot(B)
    X = C.dot(D)
    x0 = X[0][0]
    y0 = X[1][0]
    return x0,y0

signal_strengths = signalStrength()
for i in range(len(signal_strengths)):
    d = calc_distance(signal_strengths[i], -41.4568, 3.6105, 1)
    distances.append(d)

print(distances)
X0,Y0 = coordinates(4.5, 4.5, 6, 3.5, 1, .5, distances=distances)
print(X0)
print(Y0)






