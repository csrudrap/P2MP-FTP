#include <stdio.h>
#include "sender.h"

/*
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
*/

int 
rdt_send(char *data, int size)
{
    // Data contains the file contents read in bytes.
    // For each char, make a stop_and_wait call.
    // For now, send the data directly to stop_and_wait.
    if (stop_and_wait(data))
    {
        // Error condition.
        printf("Function rdt_send: Non zero return from stop_and_wait.\n");
    }
     
}

int 
stop_and_wait(char *data)
{
    // For now, take char *data. Eventually, just a char because it will be one byte.
    // Start a timer. Send the data on a UDP socket. Wait for ACK.
    // If the ACK comes back, print a success message and return.
    // If the ACK does not come back, try again. 
    // Timer runs as a thread. 
}

