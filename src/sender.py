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
seg_type = 0b0101010100000000
last_seg_type = 0b0101010111111111 
timer = None
timer_expired = True
seq = 0
ack_identifier = 0b1010101000000000


def all_ips(ips):
    # To-Do: Do an IP address check.
    return True


def calculate_checksum():
    # calculate checksum on buff
    return 0b1010110101110100   # Remove this line and return something valid.


def create_socket_and_connect(dest_hostname, dest_port):
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
    except error:
        print "Socket could not be created"
        sys.exit(1)
    sock.connect((dest_hostname, dest_port))
    return sock


def ftp_init(ips):
    global receivers
    global timer
    global timer_expired
    for i in ips:
        receivers[i] = False
    buf = ""
    timer_expired = True
    timer = Timer(0.2, update_timer)
    seq = 0


def build_segment(is_last_byte):
    global receivers
    global timer
    global timer_expired
    global last_seg_type
    global seg_type
    
    data_identifier = last_seg_type if is_last_byte else seg_type
    checksum = calculate_checksum()
    return struct.pack('iHH' + str(len(buf)) + 's', seq, checksum, data_identifier, buf)


def stop_and_wait_worker(ip, is_last_byte):
    # Send the segment to the receiver. 
    # If data is not received, keep trying while timer_expired is false.
    # If ack is incorrectly received, do not update the receiver dictionary, simply return.
    
    global timer_expired
    global receivers

    data_received = False
    sock = create_socket_and_connect(ip, 66500)
    sock.sendall(build_segment(is_last_byte))
    while timer_expired == False and data_received == False:
        try:
            ack = sock.recv(4096)
            if ack is not None:
                data_received = True
            unpacked_ack = unpack('iHH', ack)
            if is_ack_correctly_received(unpacked_ack):  # Check if data identifier is correct, checksum is correct.
                receivers[ip] = True
        except error:
            print "Error in sock.recv", error  # What do we put here?
     

def is_ack_correctly_received(ack):
    # Ack is correctly received if the identifier is 1010101000000000.
    # ack is of type tuple
    if len(ack) < 3:
        return False
    return ack[2] == ack_identifier


def send_data(is_last_byte):
    # Start timer
    # Spawn threads for each IP in receivers.
    # Wait for each thread to finish, call join.
    global timer
    global receivers
    global timer_expired
    timer.start()
    timer_expired = False
    recv_threads = []
    for i in range(len(receivers.keys())):
        if receivers[i] == False:
            new_thread = threading.Thread(target=stop_and_wait_worker, args=(receivers.keys()[i], is_last_byte,))
            new_thread.start()
            recv_threads.append(new_thread)
    for i in recv_threads:
        i.join()
    # If any of the receivers haven't sent ACKs yet, return False so that this function can be called again.
    for i in receivers.keys():
        if receivers[i] == False:
            return False
    return True


# To-Do: Doc string.
# data: String, is_last_byte: boolean
def stop_and_wait(data, is_last_byte):
    global buf
    global mss
    global seq
    buf += data
    if len(buf) == mss:
        # Buffer is fully filled up.
        # Send the buffer over to the receivers
        current_segment_done = False
        while current_segment_done == False:
            current_segment_done = send_data(is_last_byte)
        if seq == 4294967295: #To-Do: Remove hardcoded value.
            seq = 0
        else:
            seq += 1
        prepare_next_segment()
                

def prepare_next_segment():
    global buf
    global timer
    global receivers
    buf = ""
    if timer.is_alive():
        timer.stop()
        print "Timer should not have been active."  # Change this to something better.
    timer = Timer(0.2, update_timer)
    for i in receivers.keys():
        receivers[i] = False
       

def update_timer():
    # set global timer_expired value to True. 
    global timer_expired
    timer_expired = True

# To-Do: Doc string. 
# file_contents: String, ips: list of IP addresses as strings.
def rdt_send(file_contents, ips):
    # Check if all entries in the ips list are IP addresses. 
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


