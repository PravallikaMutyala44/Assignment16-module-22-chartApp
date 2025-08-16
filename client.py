import socket
from threading import Thread

import os

class Client:
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))
        self.name = input("Enter your name: ")

        self.talk_to_server()

    def talk_to_server(self):
        self.socket.send(self.name.encode())
        Thread(target=self.receive_message).start()
        self.send_message()
    
    def send_message(self):
        while True:
            client_input = input("")
            if client_input.strip().lower() == "bye":
                self.socket.send("bye".encode())
                self.socket.close()
                break
            else:
                client_message =client_input
                self.socket.send(client_message.encode())

            
    def receive_message(self):
        while True:
            try:
                server_message = self.socket.recv(1024).decode()
                print("\033[1;31;40m" + server_message + "\033[0m")
            except:
                os.exit(0)

if __name__ == '__main__':
    Client('localhost', 5000)