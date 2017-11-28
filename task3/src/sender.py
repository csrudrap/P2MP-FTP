import socket
import sys
import struct
import threading
from threading import Timer
import time


receivers = {}
mss = 0
buf = ""
seg_type = 0b0101010100000000
last_seg_type = 0b0101010111111111 
timer = None
timer_expired = True
seq = 0
ack_identifier = 0b1010101010101010
port_num = 65530


def calculate_checksum():
    # calculate checksum on buff
    return 0b1010110101110100   # Remove this line and return something valid.


def create_socket_and_connect():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except Exception as e:
        print "Socket could not be created"
        sys.exit(1)
    sock.settimeout(0.1)
    return sock


def ftp_init(ips):
    global receivers
    global timer
    global timer_expired
    global seq
    for i in ips:
        receivers[i] = False
    buf = ""
    timer_expired = True
    timer = Timer(0.8, update_timer)
    if timer.is_alive():
        timer.cancel()
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
    global port_num
    data_received = False
    sock = create_socket_and_connect()
    sock.sendto(build_segment(is_last_byte), (ip, port_num))
    while timer_expired == False and data_received == False:
        try:
            ack = sock.recvfrom(4096)
            if ack is not None:
                data_received = True
            unpacked_ack = struct.unpack('iHH', ack[0])
            if is_ack_correctly_received(unpacked_ack):  # Check if the ack received is valid.
                receivers[ip] = True
        except Exception as e:
            pass    # Socket timeout may occur. Go back to the while loop without printing anything.
     

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
    if timer.is_alive():
        timer.cancel()
    timer = Timer(0.8, update_timer)
    timer.start()
    timer_expired = False
    recv_threads = []
    for i in range(len(receivers.keys())):
        if receivers[receivers.keys()[i]] == False:
            new_thread = threading.Thread(target=stop_and_wait_worker, args=(receivers.keys()[i], is_last_byte,))
            new_thread.start()
            recv_threads.append(new_thread)
    for i in recv_threads:
        i.join()
    for i in receivers.keys():
    # If any of the receivers haven't sent ACKs yet, return False so that this function can be called again.
        if receivers[i] == False:
            return False
    if timer.is_alive():
        timer.cancel()
        timer = Timer(0.8, update_timer)
    return True


# To-Do: Doc string.
# data: String, is_last_byte: boolean
def stop_and_wait(data, is_last_byte):
    global buf
    global mss
    global seq
    buf += data
    if len(buf) == mss or is_last_byte:
        # Buffer is fully filled up or this is the last byte. In the latter case, send although
        # buf size is less than mss
        # Send the buffer over to the receivers
        current_segment_done = False
        while current_segment_done == False:
            current_segment_done = send_data(is_last_byte)
        if seq == 4294967295:   # Value of 2 to the power of 32.
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
        timer.cancel()
    timer = Timer(0.8, update_timer)
    for i in receivers.keys():
        receivers[i] = False
       

def update_timer():
    # set global timer_expired value to True. 
    global timer_expired
    global seq
    timer_expired = True
    print "Timeout, sequence number = {}".format(seq)


# file_contents: String, ips: list of IP addresses as strings.
def rdt_send(file_contents, ips): 
    ftp_init(ips)
    for i in range(len(file_contents)):
        if i == len(file_contents) - 1:
            # This is the last byte to be sent.
            stop_and_wait(file_contents[i], True)
        else:
            stop_and_wait(file_contents[i], False)


def main():
    if len(sys.argv) < 4:
        print "Please input 4 arguments: python sender.py <FILENAME: STRING> <MSS: INT> <PORT_NUM: INT>"
        sys.exit(1)
    if not sys.argv[1] or '../' in sys.argv[1]:
        print "Please input the filename correctly."
        sys.exit(1)
    f = open("../files/" + sys.argv[1], "r")
    file_contents = f.read()
    ips = open("../files/ips.txt", "r").read().split('\n')[:-1]
    global mss
    mss = int(sys.argv[2])
    global port_num
    port_num = int(sys.argv[3])
    init_time = time.time()
    rdt_send(file_contents, ips)
    final_time = time.time()
    print "Time taken:", final_time - init_time
    
if __name__ == "__main__":
    main()


