#include <stdio.h>
#include "sender.h"

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

