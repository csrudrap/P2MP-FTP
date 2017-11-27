# This will contain some test functions for the receiver side
# the functionality tested here will then be implemented in receiver.c
import random
import struct
import socket
import os

int currseqNum # this is a global value which keeps record of the current sequence number

#struct segmentACK{
#	int seqNum[32] # sequence number of the packet
#	char dataACK[16] # data field that is all zeroes
#	char packetType[16] # 10101010101010 - indicating that is an ACK packet
#}
#data = "45 00 00 47 73 88 40 00 40 06 a2 c4 83 9f 0e 85 83 9f 0e a1" # test data

def build_ACKsegment:
    seqNum = currseqNum;
    dataACK = "0000000000000000"
    packetType = "1010101010101010"
    return struct.pack('iHH',seqNum,dataACK,packetType)

def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def calcuateChecksum(): #calculate the checksum of the incoming packet
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff

data = data.split()
data = map(lambda x: int(x,16), data)
data = struct.pack("%dB" % len(data), *data)

print ' '.join('%02X' % ord(x) for x in data)
print "Checksum: 0x%04x" % calculateChecksum(data)

def dropPacket(float p): # drop packet according to a probability p - here p is between 0 and 1
    r = random.uniform(0,1)
    if(r<=p):
        return 0 # drop packet
    else:
        return 1 # retain the packet

def ftpInit(port):
    s = socket.socket()
    s.bind(('',port)
    s.listen(1)
    c,addr = s.accept()
    print("Got connection from: %s",addr)

    while 1:
        data = c.recv(BUFFER_SIZE)
        if not data:
            break
        print("Received data:%s",data)
    return s

def main:
# socket should be open for receiving packets
    sock = ftpInit()
#drop packet according to the probability p which is read from the command line

#once packet is received, read the fields inside the packet, calculate checksum
# the function should check whether the packet is in sequence
#if it is in sequence it sends an ACK segment
# after that it writes the received data into a file
# if the packet received is out of sequence, and ACK for the last received in sequence packet is sent
# if the checksum is incorrect, the receiver does nothing

