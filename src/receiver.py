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


def build_segment_ack(data):
    seqNum = data[0]
    dataACK = 0b0000000000000000
    packetType = 0b1010101010101010
    return struct.pack('iHH', seqNum, dataACK, packetType)


def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)


def verify_checksum(msg):
    # Referred from stackoverflow.
    return True
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
    global cur_seq
    # Header length is 4 + 2 + 2 = 8
    n = len(raw_data) - 8
    data = struct.unpack('iHH' + str(n) + 's', raw_data) # data is a tuple
    if not dropSegment(data, p):
        # Retain the segment, process it.
        # Check if data has 4 fields at least.
        print "SEQ RECVD IS: ", data[0]
        if data[0] != cur_seq + 1:
            print "Segment received not in sequence for seq number {}".format(data[0])
            return False
        else:
            if not verify_checksum(data):
                print "Checksum invalid, discarding segment for seq number {}".format(data[0])
                return False
            else:
                append_to_file(data[3])
                seg = build_segment_ack(data)
                sock.sendto(build_segment_ack(data), addr)
                cur_seq += 1
                return True
    else:
        # Segment is discarded based on probability.
        return False


def append_to_file(data):
    global buf
    buf += data

def ftp_recv(port, p):
    sock = create_and_bind_socket(port)
    while True:
        # BUFFER_SIZE is the maximum limit on the size of the segment that the server will receive.
        data, addr = sock.recvfrom(BUFFER_SIZE)
        # print "Got connection from: %s", addr
        if not data:
            continue
        #print "Received data:%s", data
        ret = process_data(sock, data, p, addr)
        # ret is True only when the segment is processed correctly and ACK is sent out.
        if is_last_segment(data) and ret:
            # After last segment is CORRECTLY processed, break out of the while True loop.
            break
        

def is_last_segment(data):
    n = len(data) - 8
    unpacked_data = struct.unpack('iHH' + str(n) + 's', data) # unpacked_data is a tuple
    data_id = unpacked_data[2]
    # We identify the last segment by 0101010111111111.
    return data_id == 0b0101010111111111


#once packet is received, read the fields inside the packet, calculate checksum
# the function should check whether the packet is in sequence
#if it is in sequence it sends an ACK segment
# after that it writes the received data into a file
# if the packet received is out of sequence, and ACK for the last received in sequence packet is sent
# if the checksum is incorrect, the receiver does nothing


def main():
    if len(sys.argv) < 4:
        print "Please input 4 arguments: python receiver.py <FILENAME: STRING> <PROBABILITY: FLOAT BETWEEN 0 and 1> <PORT_NUM: INT>"
        sys.exit(1)
    filename = sys.argv[1]
    p = float(sys.argv[2])
    port = int(sys.argv[3])
    global cur_seq
    cur_seq = -1
    ftp_recv(port, p)
    with open(filename, "w") as f:
        f.write(buf)
    

if __name__ == "__main__":
    main()
