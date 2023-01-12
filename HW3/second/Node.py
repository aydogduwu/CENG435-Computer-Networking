import socket
import time
import json
import threading
from sys import argv


class Node:
    total_nodes = None  # total number of nodes in the network
    host = '127.1.0.0'  # host name
    updated = False     # flag to indicate if distance vector has been updated
    done = False        # flag to indicate if listener has finished

    def __init__(self, port, cost):
        self.port = port
        self.cost = cost
        self.neighbors = {}
        self.distance_vector = {}

    def cost_reader(self, cost_file):
        with open(cost_file) as f:
            lines = f.readlines()
            self.total_nodes = int(lines[0])

            # initialize distance vector and neighbors
            for line in lines[1:]:
                port, cost = line.split()
                self.neighbors[int(port)] = int(cost)
                self.distance_vector[int(port)] = int(cost)

            # if node is not a neighbor, set distance to infinity, where ports start from 3000
            for i in range(3000, 3000 + self.total_nodes):
                if i not in self.neighbors and i != self.port:
                    self.distance_vector[i] = float('inf')
                if i == self.port:
                    self.distance_vector[i] = 0

    def distance_vector_sender(self):
        time.sleep(1)                   # wait for listener to start
        for port in self.neighbors:     # send the node’s distance vector to every immediate neighbor for first time
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, port))
            sock.send(json.dumps(self.distance_vector).encode())
            sock.close()

        while not self.done:
            if self.updated:  # send distance vector to neighbors if it has been updated
                for port in self.neighbors:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((self.host, port))
                    sock.send(json.dumps(self.distance_vector).encode())
                    sock.close()
                self.updated = False  # reset updated flag

    def distance_vector_listener(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen()
        sock.settimeout(5)
        try:
            while True:
                conn, addr = sock.accept()
                data = conn.recv(1024)
                distance_vector = json.loads(data.decode())  # receive distance vector from neighbor
                conn.close()  # close connection
                incoming_port = int([port for port in distance_vector if distance_vector[port] == 0][0])  # get port of neighbor
                distance_vector = {int(key): value for key, value in distance_vector.items()}  # convert keys to int
                self.update_distance_vector(distance_vector, incoming_port)

                sock.settimeout(5)  # reset timeout
        except Exception:
            self.done = True  # set done flag to true
            sock.close()  # close socket
            self.print_distance_vector()  # print distance vector

    def update_distance_vector(self, distance_vector, incoming_port):
        for port in distance_vector:  # attempt to update the distance vector by using received distance vectors
            if self.distance_vector[port] > self.distance_vector[incoming_port] + distance_vector[port]:
                self.distance_vector[port] = self.distance_vector[incoming_port] + distance_vector[port]
                self.updated = True

    def print_distance_vector(self):
        for port in self.distance_vector:   # print distance vector
            print(f'{self.port} -{port} | {self.distance_vector[port]}')

    def run(self):
        # create 2 threads to send and receive distance vectors
        sender_thread = threading.Thread(target=self.distance_vector_sender)
        listener_thread = threading.Thread(target=self.distance_vector_listener)

        # start threads
        sender_thread.start()
        listener_thread.start()

        # wait for threads to finish
        sender_thread.join()
        listener_thread.join()


def main():
    # read port and cost from command line
    port = int(argv[1])
    cost_file = str(argv[1])+'.costs'

    # create node and read cost file
    node = Node(port, cost_file)
    node.cost_reader(cost_file)

    # run node
    node.run()


if __name__ == '__main__':
    main()
