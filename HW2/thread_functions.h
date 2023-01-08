#include <cstdio>
#include <cstdlib>
#include <unistd.h>
#include <cerrno>
#include <cstring>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <thread>
#include <string>
#include <iostream>

#define MAXBUFLEN 100
#define SERVERPORT "4950"    // the port users will be connecting to



int sockfd, sockfd2;
struct addrinfo hints, *servinfo, *p;
struct addrinfo hints2, *servinfo2, *p2;
int rv, rv2;
int numbytes2;
int numbytes;


struct sockaddr_storage their_addr;
socklen_t addr_len;

void send_thread();
void receive_thread();