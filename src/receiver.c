#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>

#define PORT 7735
#define BUFFERSIZE 1500

int main(int argc, char **argv){

	struct sockaddr_in myaddr;      // our address 
	struct sockaddr_in remaddr;     // remote address
        socklen_t addrlen = sizeof(remaddr);            // length of addresses 
        int recvlen;                    // # bytes received 
        int sock;                         // our socket 
        unsigned char buf[BUFFERSIZE];     // receive buffer

	//creating a UDP socket
	sock = socket(AF_INET,SOCK_DGRAM,0);
	
	if(sock < 0)
	{
		perror("Cannot create socket!\n");
		return 0;
	}
	
	//binding the socket to any valid IP address and a specific port
	
	memset((char *)&myaddr, 0, sizeof(myaddr));
        myaddr.sin_family = AF_INET;
        myaddr.sin_addr.s_addr = htonl(INADDR_ANY);
        myaddr.sin_port = htons(PORT);

	if(bind(sock, (struct sockaddr *)&myaddr,sizeof(myaddr)) < 0){
		perror("Socket binding has failed!\n");
		return 0;
	}
	
	while(1){
	
	printf("Waiting on PORT:%d",PORT);
	recvlen = recvfrom(sock,buf,BUFFERSIZE,0,(struct sockaddr *)&remaddr,&addrlen);
	printf("Receieved number of bytes: %d\n",recvlen);
	
	if(recvlen > 0){
		buf[recvlen]=0;
		printf("Received Message is:%s\n",buf);
	}
}
}


