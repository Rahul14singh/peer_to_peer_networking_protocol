import socket
import threading
import os
import glob
import time
import logging

# Rahul main contribution

class Peer:
    def __init__(self, host, port, known_peers):
        self.current_id = "Curiosity_Rover"
        self.host = host
        self.port = port
        self.known_peers = known_peers  # List of known peers in the format (host, port)
        self.peers = []  # List to store connected peers
        logging.basicConfig(level=logging.DEBUG)
        file_handler = logging.FileHandler("debug.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logging.getLogger().addHandler(file_handler)

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
            self.peers.append((host, port, client))
            print(f"Connected to {host}:{port}")
        
        except Exception as e:
            print(f"Error connecting to peer: {e}")

    def delete_file(self, file_name, root_directory):
        # Create the file path pattern
        file_path_pattern = os.path.join(root_directory, file_name)

        # Use glob to find all matching files
        matching_files = glob.glob(file_path_pattern, recursive=True)

        if not matching_files:
            print(f"No matching files found for {file_name} in {root_directory}")
            return

        # Delete each matching file
        for file_path in matching_files:
            try:
                os.remove(file_path)
                logging.debug(f"Deleted file: {file_path}")
            except Exception as e:
                logging.debug(f"Error deleting file {file_path}: {e}")

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"Received message: {data}")

                if "Delete" in data:
                    file_to_delete = data.split("Delete")[1].strip()
                    self.delete_file(file_to_delete, "/users/pgrad/zhangj20/group24/data_test")
                    self.broadcast_message(self.current_id + " : Deleted "+ data.split(" ")[-1].strip(), 20, 450)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def broadcast_message(self, message, repetitions=20, interval=450):

        for peer in self.peers:
            _, _, client = peer
            try:
                for _ in range(1):
                    client.send(message.encode('utf-8'))
                    time.sleep(20)
            except Exception as e:
                print(f"Error sending message to {peer}: {e}")

if __name__ == "__main__":
    # Define your host, port, and a list of known peers
    current_id = "Curiosity_Rover"
    current_host = "10.35.70.12"
    current_port = 33343
    known_peers = [("10.35.70.31", 33341), ("10.35.70.24", 33342)]

    # Create a Peer instance
    peer = Peer(current_host, current_port, known_peers)

    peer.start()

