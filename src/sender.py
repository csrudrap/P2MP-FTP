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

# rdt_send will receive the entire data; fread is called by the client program and the buffer is passed to rdt_send. 
# rdt_send runs a loop for each byte and passes each byte to stop_and_wait(). 
# stop_and_wait(): Function in a separate file.
#       Keep a global buffer of header + data size. ftp_init(size) can be called by rdt_send() which will send the Segment
#       size and malloc that much data. If the buffer already exists, free and then allocate. Make this buffer static.
#       
#       Read in the values of IP addresses from a file. First line can be the number of receivers n, and the next n lines can
#       have IP addresses. Build an array and pass the array to the function ftp_init(), in addition to the array size.
#       Copy this array into a static array of the same size.
#       In ftp_init, create another array of the same size with all zeroes. Make it static.
#       
#       Header is created with the checksum at the beginning, set to all 1s. This will be changed at the end.
#
#       When stop_and_wait() is called with a byte of data, a check is done to see if the buffer is completely filled. If not,
#       the byte is added to the buffer. 
#       If filled, the data must be sent out.
#       While sending the data, call a send_current_segment() function, which starts a timer as a separate thread.
#       It must also create a thread to send data to each receiver.


import socket
import sys
import struct
from threading import Timer
receivers = {}
mss = 0
buf = ""
seg_type = 0b1010101000000000
last_seg_type = 0b1010101011111111 
timer = None
timer_expired = True


def all_ips(ips):
    # To-Do: Do an IP address check.
    return True


def ftp_init(ips):
    for i in ips:
        receivers[i] = 0
    global buf
    buf = ""
    global timer_expired
    timer_expired = True
    global timer
    timer = Timer(0.2, update_timer)


def stop_and_wait_worker(ip, is_last_byte):
    # create_socket_and_send()
    # while timer_expired is false, try to recv bytes (4096, say)
    # process_ack() if ack is received. That function simply sets the value in receivers[ip] to 1.
    # if timer_expired is true and ack isn't received,      


def send_data(is_last_byte):
    # Start timer
    # Spawn threads for each IP in receivers.
    # Wait for each thread to finish, call join.
    # Then, set the buffer to "" and set receivers[i] to 0 for all receivers.
    timer.start()
    for i in receivers:
        threading.Thread(target=stop_and_wait_worker, args=(i, is_last_byte,)).start()
    # JOIN.
    

# To-Do: Doc string.
# data: String, is_last_byte: boolean
def stop_and_wait(data, is_last_byte):
    buf += data
    if len(buf) == mss:
        # Buffer is fully filled up.
        # Send the buffer over to the receivers
        send_data(is_last_byte)
            

# To-Do: Doc string. 
# file_contents: String, ips: list of IP addresses as strings.
def rdt_send(file_contents, ips):
    # Check if all entries in the 
    if not all_ips(ips):
        print "IP addresses of receivers incorrect. Please check the file and try again."
        sys.exit(1)
    ftp_init(ips)
    for i in range(len(file_contents):
        if i == len(file_contents) - 1:
            stop_and_wait(file_contents[i], True)
        else:
            stop_and_wait(file_contents[i], False)


def main():
    if not sys.argv[2] or '../' in sys.argv[2]:
        print "Please input the filename correctly."
        sys.exit(1)
    f = open("../files/" + sys.argv[2], "r")
    file_contents = f.read()
    # To-Do: Check if the ips.txt file exists and exit if not.
    ips = open("../files/ips.txt", "r").read().split('\n')
    global mss
    mss = int(sys.argv[3])
    rdt_send(file_contents, ips)
    
    
if __name__ == "__main__":
    main()


