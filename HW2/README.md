# CENG435 - THE2

My implementation includes simple UDP networking without Go-Back-N. It is built on top of the code examples on http://beej.us/guide/bgnet/.

It includes 2 threads for server and 2 threads for client.

Both server and client are able to take and send messages. If a message to be sent is longer than 16 bytes, it is divided into 16 bytes chunks.

Both server and client stop after three consecutive newline characters.


