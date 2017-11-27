// This will contain some test functions for the receiver side
// the functionality tested here will then be implemented in receiver.c

#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>

#define PORT 7735
#define BUFFERSIZE 1500

int currseqNum; // this is a global value which keeps record of the current sequence number

struct segmentACK{
	char seqNum[32]; // sequence number of the packet
	char dataACK[16]; // data field that is all zeroes
	char packetType[16]; // 10101010101010 - indicating that is an ACK packet
};

int calcuateChecksum(); //calculate the checksum of the incoming packet
int dropPacket(float p); // drop packet according to a probability p - here p is between 0 and 1

int dropPacket(float p){// here p is the probability fetched from the command line:: generalistic probabilistic error in implementing our protocol
srand(time(NULL));
float r = (double)rand()/(double)RAND_MAX;

if(r <= p)
	return 0; // drop this packet
else
	return 1; // keep this packet
}

int main(int argc, char **argv){

// socket should be open for receiving packets

//drop packet according to the probability p which is read from the command line

//once packet is received, read the fields inside the packet, calculate checksum
// the function should check whether the packet is in sequence
//if it is in sequence it sends an ACK segment
// after that it writes the received data into a file
// if the packet received is out of sequence, and ACK for the last received in sequence packet is sent
// if the checksum is incorrect, the receiver does nothing


}
