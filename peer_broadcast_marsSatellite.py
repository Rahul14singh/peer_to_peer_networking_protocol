import socket
import threading
import os
import glob
import time
import logging

# Rahul main contribution

class Peer:
    def __init__(self, host, port, known_peers):
        self.current_id = "Mars_Satellite"
        self.host = host
        self.port = port
        self.known_peers = known_peers  # List of known peers in the format (host, port)
        self.peers = []  # List to store connected peers
        self.message_cache = []  # Cache to store broadcast messages
        self.message_receivers = {}  # Dictionary to track receivers of each message
        self.lock = threading.Lock()  # Lock for thread safety
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

            # Send any cached messages to the newly connected peer
            with self.lock:
                for cached_message, receivers in self.message_receivers.items():
                    if host not in receivers:
                        client.send(cached_message.encode('utf-8'))
                        print(f"Sent cached message to {host}:{port}")
                        time.sleep(20)
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
    
    def send_deleted_message(self, host, port, deleted_file, repetitions=20, interval=450):
        message = f"{self.current_id} : Deleted {deleted_file}"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((host, port))
                for _ in range(1):
                    client_socket.send(message.encode('utf-8'))
                    print(f"Sent deleted message to {host}:{port}")
                    time.sleep(20)
        except Exception as e:
            print(f"Error sending deleted message: {e}")

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
                        file_name = data.split(" ")[-1].strip()
                        if file_name in self.message_receivers.keys():
                            device = data.split(":")[0].strip()
                            if device not in self.message_receivers[file_name]:
                                self.message_receivers[file_name].append(device)
                        else:
                            self.message_receivers[file_name] = [data.split(":")[0].strip()]

                elif "Delete" in data:
                    file_name = data.split(" ")[-1].strip()
                    self.delete_file(file_name, "/users/pgrad/burder/group24/data_test")
                    self.broadcast_message(self.current_id + " : Delete "+ file_name)
                    
                    # Update the message receivers
                    with self.lock:
                        if file_name in self.message_receivers.keys():
                            if self.current_id not in self.message_receivers[file_name]:
                                self.message_receivers[file_name].append(self.current_id)
                            else:
                                self.message_receivers[file_name] = [self.current_id]

            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def broadcast_message(self, message):
        if message not in self.message_cache:
            with self.lock:
                self.message_cache.append(message)  # Cache the message

        for peer in self.peers:
            _, _, client = peer
            try:
                client.send(message.encode('utf-8'))
                time.sleep(20)
            except Exception as e:
                print(f"Error sending message to {peer}: {e}")

    def check_and_remove_messages(self):
        devices_to_check = set(["Mars_Satellite", "Mars_Rover", "Curiosity_Rover", "Lander_Module"])

        def broadcast_cached_messages():
            for cached_message in self.message_cache:
                self.broadcast_message(cached_message)
                time.sleep(20)

        while True:
            time.sleep(20)  # Sleep for 7.5 minutes
            
            logging.debug(self.message_receivers)
            logging.debug(self.message_cache)
            
            with self.lock:
                messages_to_remove = []
                for cached_message, receivers in self.message_receivers.items():
                    received_devices = set([peer for peer in receivers])

                    # Check if both sets have the same values
                    if devices_to_check == received_devices:
                        messages_to_remove.append(cached_message)
                        logging.debug("Removed")

                for message in messages_to_remove:
                    # Send a deleted message to 10.35.70.24:33340
                    self.send_deleted_message("10.35.70.24", 33340, message, repetitions=20, interval=450)
                    
                    self.message_receivers.pop(message)
                    self.message_cache = [mess for mess in self.message_cache if message not in mess]
                    print(f"Removed message from cache: {message}")
            
            logging.debug(self.message_receivers)
            logging.debug(self.message_cache)
           
            # Run the broadcasting of cached messages in a separate thread
            broadcast_thread = threading.Thread(target=broadcast_cached_messages)
            broadcast_thread.start()

if __name__ == "__main__":
    # Define your host, port, and a list of known peers
    current_id = "Mars_Satellite"
    current_host = "10.35.70.31"
    current_port = 33341
    known_peers = [("10.35.70.12", 33343), ("10.35.70.28", 33344), ("10.35.70.42", 33345)]

    # Create a Peer instance
    peer = Peer(current_host, current_port, known_peers)

    # Start the check_and_remove_messages thread
    threading.Thread(target=peer.check_and_remove_messages).start()

    peer.start()
