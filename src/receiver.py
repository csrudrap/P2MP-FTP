# This will contain some test functions for the receiver side
# the functionality tested here will then be implemented in receiver.c
import random
import struct
import socket
import os
import sys

cur_seq = -1 # is a global value which keeps record of the current seq num to prevent out-of-order packets.
BUFFER_SIZE = 8192 # Arbitrarily chosen maximum limit.
buf = ""

#struct segmentACK{
#	int seqNum[32] # sequence number of the packet
#	char dataACK[16] # data field that is all zeroes
#	char packetType[16] # 10101010101010 - indicating that is an ACK packet
#}
#data = "45 00 00 47 73 88 40 00 40 06 a2 c4 83 9f 0e 85 83 9f 0e a1" # test data

def build_segment_ack(data):
    seqNum = data[0]
    dataACK = 0b0000000000000000
    packetType = 0b1010101010101010
    return struct.pack('iHH', seqNum, dataACK, packetType)

def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def verify_checksum(msg):
    return True # FIX THIS
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        s = carry_around_add(s, w)
    if (~s & 0xffff) == 0x0000:
        return True
    else:
        return False


#data = data.split()
#data = map(lambda x: int(x,16), data)
#data = struct.pack("%dB" % len(data), *data)

#print ' '.join('%02X' % ord(x) for x in data)
#print "Checksum: 0x%04x" % calculateChecksum(data)

def dropSegment(data, p): # drop packet according to a probability p - here p is between 0 and 1
    return False    # FIX THIS
    r = random.uniform(0, 1)
    if r <= p:
        print "Packet loss, sequence number = {}".format(data[0])
        return True # drop packet
    else:
        return False # retain the packet


def create_and_bind_socket(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except Exception as e: # Change this line.
        print "Socket could not be created", e
        sys.exit(1)
    if sock == None:
        print "Socket is None! Exiting."
        sys.exit(1)
    else:
        try:
            sock.bind(('', port))
        except Exception as e:
            print e.message
            print "Could not bind socket to port! Exiting"
            shutdown_and_close(sock)
            sys.exit(1)
    return sock


def shutdown_and_close(sock):
    try:
        sock.shutdown(socket.SHUT_RDWR)
        print "Socket shutdown successfully."
    except Exception as e:
        print e.message, "Couldn't shutdown the socket on the server."
    try:
        sock.close()
    except Exception as e:
        print e.message, "Couldn't close the socket"


def process_data(sock, raw_data, p, addr):
    #To-Do: Find the size in a better way.
    global cur_seq
    n = len(raw_data) - 8
    data = struct.unpack('iHH' + str(n) + 's', raw_data) # data is a tuple
    if not dropSegment(data, p):
        # Retain the segment, process it.
        # Check if data has 4 fields at least.
        if data[0] != cur_seq + 1:
            print "Segment received not in sequence for seq number {}".format(data[0])
        else:
            if not verify_checksum(data):
                print "Checksum invalid, discarding segment for seq number {}".format(data[0])
            else:
                append_to_file(data[3])
                seg = build_segment_ack(data)
                sock.sendto(build_segment_ack(data), addr)
                cur_seq += 1


def append_to_file(data):
    global buf
    buf += data

def ftp_recv(port, p):
    sock = create_and_bind_socket(port)
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        print "Got connection from: %s", addr
        # BUFFER_SIZE is the maximum limit on the size of the segment that the server will receive.
        if not data:
            continue
        print "Received data:%s", data
        process_data(sock, data, p, addr)
        if is_last_segment(data):
            break
        

def is_last_segment(data):
    n = len(data) - 8
    unpacked_data = struct.unpack('iHH' + str(n) + 's', data) # unpacked_data is a tuple
    data_id = unpacked_data[2]
    return data_id == 0b0101010111111111

#drop packet according to the probability p which is read from the command line

#once packet is received, read the fields inside the packet, calculate checksum
# the function should check whether the packet is in sequence
#if it is in sequence it sends an ACK segment
# after that it writes the received data into a file
# if the packet received is out of sequence, and ACK for the last received in sequence packet is sent
# if the checksum is incorrect, the receiver does nothing


def main():
    port = 65530
    p = 0.5
    global cur_seq
    cur_seq = -1
    ftp_recv(port, p)
    print buf
    

if __name__ == "__main__":
    main()
