import socket
from threading import Thread

class Server:
    Clients=[]


    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen()
        print("server waiting for connection...")

    def listen(self):
        while True:
            client_socket, address = self.socket.accept()
            print("Connection from: " + str(address))

            client_name= client_socket.recv(1024).decode()
            client={'client_name': client_name, 'client_socket': client_socket}

            self.broadcast_message(client_name,client_name + " has joined the chat~")

            Server.Clients.append(client)
            Thread(target= self.handle_new_client, args = (client, )).start()

    def handle_new_client(self, client):
        client_name = client['client_name']
        client_socket = client['client_socket']

        while True:
            try:
                client_message = client_socket.recv(1024).decode()

                if not client_message:
                    continue
                if client_message.strip().lower() == "bye" or not client_message.strip():
                    self.broadcast_message(client_name + " has left the chat!!!")
                    Server.Clients.remove(client)
                    client_socket.close()
                    break
                elif client_message.lower() == "shutdown":
                        self.broadcast_message("SERVER", "Server is shutting down!")
                        self.shutdown_server()
                        break
                else:
                    self.broadcast_message(client_name, client_message)
            except:
                Server.Clients.remove(client)
                client_socket.close()
                break

    def broadcast_message(self,sender_name, message):
        for client in Server.Clients:
            client['client_socket'].send(f"{sender_name}: {message}".encode())
        print(f"{sender_name}: {message}")


if __name__ == '__main__':
    server = Server('localhost', 5000)
    server.listen()
