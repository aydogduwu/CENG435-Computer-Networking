#include "thread_functions.h"

/*
 * Function: send_thread
 *
 * This function is the thread that sends the data.
 *
 * It is called by the main function.
 */
void send_thread() {
    // if 2 consecutive enters are pressed, the program will exit
    int consecutive_enters = 0;
    while(true) {
        // take input data from user
        std::string input;
        if(consecutive_enters == 2) {
            // if 2 consecutive enters are pressed, the program will exit
            break;
        }
        std::getline(std::cin, input);
        if(input == "") {
            consecutive_enters++;
        } else {
            consecutive_enters = 0;
        }

        // convert the string to a char array
        char *input_char = new char[input.length() + 2];
        strcpy(input_char, input.c_str());
        input_char[input.length()] = '\n';
        input_char[input.length() + 1] = '\0';

        // if the input is longer than 16 bytes, divide it into 16 byte chunks
        if (strlen(input_char) > 16) {
            int i = 0;
            while (i < strlen(input_char)) {
                char *input_char_16 = new char[17];
                strncpy(input_char_16, input_char + i, 16);
                input_char_16[16] = '\0';
                if ((numbytes = sendto(sockfd, input_char_16, strlen(input_char_16), 0,
                                       p->ai_addr, p->ai_addrlen)) == -1) {
                    perror("talker: sendto");
                    exit(1);
                }
                i += 16;
                if (input != ""){
                    consecutive_enters = 0;
                }
                // delete the char array
                delete[] input_char_16;
            }
            // delete the char array
            delete[] input_char;
        }

        // if the input is 16 bytes or fewer, send it as is
        else {
            if ((numbytes = sendto(sockfd, input_char, strlen(input_char), 0,
                                   p->ai_addr, p->ai_addrlen)) == -1) {
                perror("talker: sendto");
                exit(1);
            }

            if (input != ""){
                consecutive_enters = 0;
            }

            // delete the char array
            delete[] input_char;
        }

    }

    // close the socket
    close(sockfd);
    // free the linked list
    freeaddrinfo(servinfo);
    // exit the thread
    exit(0);

}

/*
 * Function: receive_thread
 *
 * This function is the thread that receives the data.
 *
 * It is called by the main function.
 */
void receive_thread() {
    // if 2 consecutive enters are pressed, the program will exit
    int consecutive_enters = 0;
    while (true) {
        char buf[MAXBUFLEN];

        addr_len = sizeof their_addr;
        if (consecutive_enters == 2) {
            break;
        }

        if ((numbytes2 = recvfrom(sockfd2, buf, MAXBUFLEN-1 , 0,
                                  (struct sockaddr *)&their_addr, &addr_len)) == -1) {
            perror("recvfrom");
            exit(1);
        }

        // check if 2 consecutive enters have been pressed
        if (buf[0] == '\n' || buf[1] == '\0') {
            consecutive_enters++;
            //printf("enter received \n");

        } else {
            consecutive_enters = 0;
        }
        //bool t = buf[0] == '\n';
        //printf("is enter: %d \n", t);

        //printf("received %d bytes, string: %s", numbytes2, buf);
        buf[numbytes2] = '\0';

        printf("%s", buf);
    }

    // close the socket
    close(sockfd2);
    // free the linked list
    freeaddrinfo(servinfo2);
    // exit the thread
    exit(0);
}