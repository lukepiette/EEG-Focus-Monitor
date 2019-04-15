
# coding: utf-8

# In[ ]:


import struct
import socket
import codecs
import time
from pygame import mixer


# In[ ]:


def _getDecDigit(digit):
    digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    for x in range(len(digits)):
        if digit.lower() == digits[x]:
            return(x)
        
def hexToDec(hexNum):
    decNum = 0
    power = 0
    
    
    for digit in range(len(hexNum), 0, -1):
        try:
            decNum = decNum + 16 ** power * _getDecDigit(hexNum[digit-1])
            power += 1
        except:
            return
    return(int(decNum))


def playFunc(num):
    
    if num == 1:
        mixer.music.load("Downloads\country.mp3")
        mixer.music.play()
        
    if num == 2:
        mixer.music.load("Downloads\classical.mp3")
        mixer.music.play()
        
    if num == 3:
        mixer.music.load("Downloads\hard_rap.mp3")
        mixer.music.play()
        
    if num == 4:
        mixer.music.load("Downloads\soft_rap.mp3")
        mixer.music.play()
        
    if num == 5:
        mixer.music.load("Downloads\chrismass.mp3")
        mixer.music.play()
        
    if num == 6:
        mixer.music.load("Downloads\zeze.mp3")
        mixer.music.play()

print('Program Initiated')
UDP_IP = "192.168.0.13"
UDP_PORT = 2003
sock = socket.socket(socket.AF_INET,  # Internet
                    socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))
digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

final = []
timer = time.clock()
stocked = []
mixer.init()
stock = []
num = 0

while num < 6:
    mixer.music.stop()
    num += 1
    playFunc(num)
    
    while True:   
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        if 'alpha_absolute' in str(data):

            newData = str(data).split(",")
            newData = newData[1].split("x")
            newData = newData[1:]
            outData = []
            for i in newData:
                outData += [hexToDec(i[:-1])]

            newerOut = []
            for i in outData:
                if type(i) == int and i > 0:
                    newerOut += [i]

            if len(newerOut) == 0:
                continue

            stock += [sum(newerOut)/len(newerOut)]

            if time.clock() - timer > 10:
                stock = sum(stock)/len(stock)
                stocked += [stock]
                stock = []
                timer = time.clock()
                break 
    
newNum = stocked.index(max(stocked))
playFunc(newNum)

print(" ")
print(" ")
print("Measuring Focus")
print("---------------")
print(" ")

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    
    if 'alpha_absolute' in str(data):
        newData = str(data).split(",")
        newData = newData[1].split("x")
        newData = newData[1:]
        outData = []
        for i in newData:
            outData += [hexToDec(i[:-1])]

        newerOut = []
        for i in outData:
            if type(i) == int and i > 0:
                newerOut += [i]
        
        if len(newerOut) == 0:
            continue

        final += [sum(newerOut)/len(newerOut)]
        
        if (time.clock() - timer) > 5:
            a = ((sum(final)/len(final))/(max(stocked)))*100
            
            if 100 > a > 60:
                print("Focused : ",a,"%")
            elif a > 100:
                print("Focused : 95%")
            else:
                print("Focused : ",a,"%")
            timer = time.clock()

