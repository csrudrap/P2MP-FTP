'''
* rdt_send will receive the entire data; fread is called by the client program and the buffer is passed to rdt_send. 
* rdt_send runs a loop for each byte and passes each byte to stop_and_wait(). 
* stop_and_wait(): Function in a separate file.
*       Keep a global buffer of header + data size. ftp_init(size) can be called by rdt_send() which will send the Segment
*       size and malloc that much data. If the buffer already exists, free and then allocate. Make this buffer static.
*       
*       Read in the values of IP addresses from a file. First line can be the number of receivers n, and the next n lines can
*       have IP addresses. Build an array and pass the array to the function ftp_init(), in addition to the array size.
*       Copy this array into a static array of the same size.
*       In ftp_init, create another array of the same size with all zeroes. Make it static.
*       
*       Header is created with the checksum at the beginning, set to all 1s. This will be changed at the end.
*
*       When stop_and_wait() is called with a byte of data, a check is done to see if the buffer is completely filled. If not,
*       the byte is added to the buffer. 
*       If filled, the data must be sent out.
*       While sending the data, call a send_current_segment() function, which starts a timer as a separate thread.
*       It must also create a thread to send data to each receiver.

'''

# Pick up a string, use pack and send it to a server. Put a header and then read only the data and unpack the data.
# Send a file with 1000 bytes in chunks of 2 (500 each).

# Trial client code, to be removed.

import sys
from socket import *
from struct import *

def create_socket_and_connect(dest_hostname, dest_port):
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
    except error:
        print "Socket could not be created"
        sys.exit(1)
    sock.connect((dest_hostname, dest_port))
    return sock

def send_msg_and_receive(msg, sock):
    sock.sendall(msg)
    try:
        data = sock.recv(8192)
    except error:
        print "Data receive failed."
        data = None
    return data


def main():
    f = open("./exec")
    file_contents = f.read()
    print len(file_contents)
    # The way pack works is that we put the format as the first argument. Here, len(file_contents) is 8608.
    # So, 'ilH8608s' is the format specifier. i for Integer (4 bytes), H for short (2 bytes), H for short (2 bytes)
    # Data length is 8608, but length of raw_pkt below is 8616, which is 8 more than the data length.
    raw_pkt = pack('iHH' + str(len(file_contents)) + 's', 6, 0b1010110101110100, 0b1010101010101010, file_contents)
    print len(raw_pkt)
    unpacked_pkt = unpack('iHH' + str(len(file_contents)) + 's', raw_pkt)
    #print unpacked_pkt
    print type(unpacked_pkt)
    print len(unpacked_pkt[3])
        

if __name__ == "__main__":
    main()



