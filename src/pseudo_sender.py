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

# sender.py has a main function which will be used to call rdt_send(), which will take the entire file string as input and
# send byte-by-byte to stop_and_wait. If index of the byte is 1 less than the length of file_contents (last byte), send True.
# Before the stop_and_wait loop in rdt_send, call ftp_init() which will initialize a dictionary with keys as receiver IP
# addresses and values as 0, indicating that the ACKs haven't come for the first segment. 

# Let there be a global buffer which stop_and_wait will fill byte-by-byte, based on the data it receives. 
# It will check the size of the buffer after adding a byte, to see if it is equal to MSS. If yes, it will call the send_data
# function that will spawn one thread per receiver to handle the sending and receiving. It will also start a timer, and the 
# timer handler function will set a global flag hasTimerExpired to True.
# Each receiver thread will wait for data if hasTimerExpired is False.
# The main thread in send_data will wait for all the threads to complete.
# A scenario in which a thread is context switched out after the if (hasTimerExpired) check can cause problems, as one more 
# additional send might happen after timeout. Care must be taken to update the dictionary associated with the CURRENT segment
# After waiting for all threads to complete, the send_data function will initialize the buffer to "" and dictionary to all 0s
# It will then return control back to stop_and_wait. 

# If this is the last segment (boolean value from rdt_send to stop_and_wait), the header should be changed.
# The 3rd field is used to distinguish between ACK and data. Use only 8 bits for that.
# If the last 8 bits are all 1s, this is the last segment.

# Pick up a string, use pack and send it to a server. Put a header and then read only the data and unpack the data.


import sys
from socket import *
from struct import *

buf = ""
MSS = 10000
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


def stop_and_wait(x, fileComplete):
    


def main():
    f = open("./exec")
    file_contents = f.read()
    for i in file_contents:
        stop_and_wait(i)
    print "Finished" 


'''    print len(file_contents)
    raw_pkt = pack('iHH' + str(len(file_contents)) + 's', 6, 0b1010110101110100, 0b1010101010101010, file_contents)
    print len(raw_pkt)
    unpacked_pkt = unpack('iHH' + str(len(file_contents)) + 's', raw_pkt)
    #print unpacked_pkt
    print type(unpacked_pkt)
    print len(unpacked_pkt[3])
'''        

if __name__ == "__main__":
    main()



