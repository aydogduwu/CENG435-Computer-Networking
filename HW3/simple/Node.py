# implementation of distance-vector routing protocol without dynamic cost  changes for arbitrary networks.
import socket
import time
from sys import argv
import json
import threading

# distance vector should be printed in the following format:
# <current node’s port> -<neighbor’s port> | distance

# For this assignment, you will implement a single Node.py that will be run separately for every
# node in the network. The nodes will then start communicating asynchronously using TCP sockets.
# When there are no more updates to be made in any of the distance vectors of the nodes, the
# algorithm will terminate.

# Every node will start by reading it’s assigned <port>.costs file from the disk to populate it’s initial
# distance vector. If you read the Section 5.2 mentioned above, you know that the initial distances
# for nodes that are not immediate neighbours of the current node are set to infinite. Every node
# will then start listening to it’s assigned port number on localhost (127.0.0.1). This port is used
# for receiving distance vector updates from the other neighbouring nodes.

# stages:
# 1. Read the neighborhood information from the .costs file
# 2. Send the node’s distance vector to every immediate neighbor
# 3. Listen for updates from the neighbors
# 4. Attempt to update the distance vector by using received distance vectors
# 5. If no update happens for 5 seconds, close all connections and print the distance vector

# cost file format:
# <total number of nodes in the network>
# <port of immediate neighbor> <cost to neighbor> newline
# create Node class to store node information


class Node:
    total_nodes = None
    host = '127.1.0.0'
    updated = False
    done = False

    def __init__(self, port, cost):
        self.port = port
        self.cost = cost
        self.neighbors = {}
        self.distance_vector = {}

    def read_cost_file(self, cost_file):
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

        # print self.distance_vector
        # print(f'Node {self.port} initialized with distance vector: {self.distance_vector}')
    # if there is an update, send the updated distance vector to all neighbors
    def send_distance_vector(self):
        # send the node’s distance vector to every immediate neighbor for first time
        time.sleep(1)
        for port in self.neighbors:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, port))
            sock.send(json.dumps(self.distance_vector).encode())
            sock.close()

        while not self.done:
            if self.updated:
                for port in self.neighbors:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((self.host, port))
                    sock.send(json.dumps(self.distance_vector).encode())
                    sock.close()
                self.updated = False

        print('asdfadf')

    def listen_for_updates(self):
        # listen for updates from neighbors
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen()
        # if there is no update for 5 seconds, close all connections and print the distance vector
        sock.settimeout(5)
        try:
            while True:
                #print(f'Node {self.port} listening for updates')
                print("first")
                conn, addr = sock.accept()
                data = conn.recv(1024)
                print("second")
                #print(f'Node {self.port} received data: {data}')
                distance_vector = json.loads(data.decode())
                conn.close()
                # find port with 0 cost
                incoming_port = int([port for port in distance_vector if distance_vector[port] == 0][0])
                # convert key values of distance vector to int
                distance_vector = {int(key): value for key, value in distance_vector.items()}
                self.update_distance_vector(distance_vector, incoming_port)
                # reset timeout
                sock.settimeout(5)
        except Exception as e:
            print(f'Node {self.port} timeout')
            self.done = True
            sock.close()
            self.print_distance_vector()

    def update_distance_vector(self, distance_vector, incoming_port):
        # attempt to update the distance vector by using received distance vectors
        print(f'Node {self.port} received distance vector from {incoming_port}: {distance_vector}')
        for port in distance_vector:
            if self.distance_vector[port] > self.distance_vector[incoming_port] + distance_vector[port]:
                self.distance_vector[port] = self.distance_vector[incoming_port] + distance_vector[port]
                self.updated = True

    def print_distance_vector(self):
        # print the distance vector
        for port in self.distance_vector:
            print(f'{self.port} -{port} | {self.distance_vector[port]}')

    def run(self):
        # create 2 threads to send and receive distance vectors
        send_thread = threading.Thread(target=self.send_distance_vector)
        receive_thread = threading.Thread(target=self.listen_for_updates)
        send_thread.start()
        receive_thread.start()
        send_thread.join()
        print(f'Node {self.port} send finished')
        receive_thread.join()
        print(f'Node {self.port} receive finished')


def main():
    # read port and cost from command line
    port = int(argv[1])
    cost_file = str(argv[1])+'.costs'

    # create node and read cost file
    node = Node(port, cost_file)
    node.read_cost_file(cost_file)

    # run node
    node.run()

def test():
    # test case
    node = Node(3000, 'simple/3000.costs')
    node2 = Node(3001, 'simple/3001.costs')
    node.read_cost_file('simple/3000.costs')
    node2.read_cost_file('simple/3001.costs')

    node2.send_distance_vector()

if __name__ == '__main__':
    main()
