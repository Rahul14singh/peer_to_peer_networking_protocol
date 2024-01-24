import socket
import threading
import os
import glob
import time

# Rahul main contribution

class Peer:
    def __init__(self, host, port, known_peers):
        self.host = host
        self.port = port
        self.known_peers = known_peers  # List of known peers in the format (host, port)
        self.peers = []  # List to store connected peers
        self.message_cache = []  # Cache to store broadcast messages
        self.message_receivers = {}  # Dictionary to track receivers of each message
        self.lock = threading.Lock()  # Lock for thread safety

    def start(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

        input("Press Enter to start connecting to peers\n")
        print("Connecting to other peers...\n")
        self.connect_to_known_peers()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()

        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = server.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def connect_to_known_peers(self):
        for peer in self.known_peers:
            host, port = peer
            self.connect_to_peer(host, port)

    def connect_to_peer(self, host, port):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, port))
            self.peers.append(client)
            print(f"Connected to {host}:{port}")

            # Send any cached messages to the newly connected peer
            with self.lock:
                for cached_message, receivers in self.message_receivers.items():
                    if host not in receivers:
                        client.send(cached_message.encode('utf-8'))
                        print(f"Sent cached message to {host}:{port}")
                        time.sleep(20)
        except Exception as e:
            print(f"Error connecting to peer: {e}")

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"Received message: {data}")

                if "Deleted" in data:
                    # Update the message receivers
                    with self.lock:
                        if data in self.message_receivers:
                            self.message_receivers[data].append(data.split(":")[0].strip())
                        else:
                            self.message_receivers[data] = [data.split(":")[0].strip()]
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def broadcast_message(self, message):
        if message not in self.message_cache:
            with self.lock:
                self.message_cache.append(message)  # Cache the message

        for peer in self.peers:
            try:
                peer.send(message.encode('utf-8'))
                time.sleep(20)
            except Exception as e:
                print(f"Error sending message: {e}")

    def check_and_remove_messages(self):
        devices_to_check = set(["Mars_Satellite", "Moon_Satellite"])

        while True:
            time.sleep(450)  # Sleep for 7.5 minutes

            with self.lock:
                messages_to_remove = []
                for cached_message, receivers in self.message_receivers.items():
                    received_devices = set([peer for peer in receivers])
                    
                    # Check if both sets have the same values
                    if devices_to_check == received_devices:
                        messages_to_remove.append(cached_message)

                for message in messages_to_remove:
                    self.message_receivers.pop(message)
                    self.message_cache.remove(message)
                    print(f"Removed message from cache: {message}")

def get_csv_to_delete(device):
    csv_files = glob.glob(os.path.join("/users/pgrad/singhr6/group24/data_test/" + device + "/*/*/*.csv"))
    delete = []
    if csv_files:
        for csv_file in csv_files:
            with open(csv_file, 'r') as file:
                line_count = sum(1 for line in file)
            if(line_count == 31):
                delete.append(csv_file)
    return delete

if __name__ == "__main__":
    # Define your host, port, and a list of known peers
    current_id = "Earth"
    current_host = "10.35.70.24"
    current_port = 33340
    known_peers = [("10.35.70.31", 33341), ("10.35.70.24", 33342)]

    # Create a Peer instance
    peer = Peer(current_host, current_port, known_peers)

    # Start the check_and_remove_messages thread
    threading.Thread(target=peer.check_and_remove_messages).start()

    peer.start()
   
    devices = ["Curiosity_Rover", "Mars_Rover", "Lander_Module", "Mars_Satellite", "Moon_Satellite"]

    for device in devices:
        delete = get_csv_to_delete(device)
        for csv in delete:
            elements = csv.split("/")
            result = "/".join(elements[-4:])

            # Set a default message to broadcast
            message_to_broadcast = current_id + ": Delete " + result
            
            print(message_to_broadcast)
            # Broadcast the default message
            peer.broadcast_message(message_to_broadcast)

            time.sleep(20)

