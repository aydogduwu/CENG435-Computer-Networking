#include "thread_functions.cpp"

using namespace std;

/*
 * This file is based on the Beej's Guide to Network Programming. See: https://beej.us/guide/bgnet/html/#datagram
 *
 * The code is modified to fit the needs of the project.
 *
 * First, creates sockets, then creates two threads to send and receive data.
 */
int main()
{
    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_INET; // set to AF_INET to use IPv4
    hints.ai_socktype = SOCK_DGRAM;

    if ((rv = getaddrinfo("172.24.0.20", SERVERPORT, &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 2;
    }

    // loop through all the results and make a socket
    for(p = servinfo; p != NULL; p = p->ai_next) {
        if ((sockfd = socket(p->ai_family, p->ai_socktype,
                             p->ai_protocol)) == -1) {
            perror("talker: socket");
            continue;
        }

        break;
    }

    if (p == NULL) {
        fprintf(stderr, "talker: failed to create socket\n");
        return 2;
    }

    memset(&hints2, 0, sizeof hints2);
    hints2.ai_family = AF_INET; // set to AF_INET to use IPv4
    hints2.ai_socktype = SOCK_DGRAM;
    hints2.ai_flags = AI_PASSIVE; // use my IP
    if ((rv2 = getaddrinfo(NULL, SERVERPORT, &hints2, &servinfo2)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv2));
        return 1;
    }

    // loop through all the results and make a socket
    for(p2 = servinfo2; p2 != NULL; p2 = p2->ai_next) {
        if ((sockfd2 = socket(p2->ai_family, p2->ai_socktype,
                              p2->ai_protocol)) == -1) {
            perror("listener_server: socket");
            continue;
        }

        if (bind(sockfd2, p2->ai_addr, p2->ai_addrlen) == -1) {
            close(sockfd2);
            perror("listener_server: bind");
            continue;
        }

        break;
    }

    if (p2 == NULL) {
        fprintf(stderr, "listener_server: failed to create socket\n");
        return 2;
    }

    // create thread for sending data and receiving data
    std::thread server_send(send_thread);
    std::thread server_receive(receive_thread);
    server_send.join();
    server_receive.join();


    return 0;
}