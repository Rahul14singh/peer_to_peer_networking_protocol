import socket
import threading
import os
import glob
import time

# Rahul main contribution

class Peer:
    def __init__(self, host, port, known_peers):
        self.current_id = "Moon_Satellite"
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
            self.peers.append((host, port, client))
            print(f"Connected to {host}:{port}")

            # Send any cached messages to the newly connected peer
            with self.lock:
                for cached_message, receivers in self.message_receivers.items():
                    if host not in receivers:
                        client.send(cached_message.encode('utf-8'))
                        print(f"Sent cached message to {host}:{port}")
        except Exception as e:
            print(f"Error connecting to peer: {e}")

    def delete_file(self, file_name, root_directory):
        # Create the file path pattern
        file_path_pattern = os.path.join(root_directory, '**', file_name)

        # Use glob to find all matching files
        matching_files = glob.glob(file_path_pattern, recursive=True)

        if not matching_files:
            print(f"No matching files found for {file_name} in {root_directory}")
            return

        # Delete each matching file
        for file_path in matching_files:
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    
    def send_deleted_message(self, host, port, deleted_file, repetitions=20, interval=450):
        message = f"{self.current_id} : Deleted {deleted_file}"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((host, port))
                for _ in range(repetitions):
                    client_socket.send(message.encode('utf-8'))
                    print(f"Sent deleted message to {host}:{port}")
                    time.sleep(interval)
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
                        if data in self.message_receivers:
                            self.message_receivers[data].append(data.split(":")[0].strip())
                        else:
                            self.message_receivers[data] = [data.split(":")[0].strip()]

                elif "Delete" in data:
                    file_to_delete = data.split("Delete")[1].strip()
                    self.delete_file(file_to_delete, "/users/pgrad/singhr6/group24/data_test")
                    # Update the message receivers
                    with self.lock:
                        if data in self.message_receivers:
                            self.message_receivers[data].append(self.current_id)
                        else:
                            self.message_receivers[data] = [self.current_id]

            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def broadcast_message(self, message):
        with self.lock:
            self.message_cache.append(message)  # Cache the message

        for peer in self.peers:
            _, _, client = peer
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message to {peer}: {e}")

    def check_and_remove_messages(self):
        devices_to_check = set(["Curiosity_Rover", "Mars_Rover", "Lander_Module", "Moon_Satellite"])

        while True:
            time.sleep(450)  # Sleep for 7.5 minutes

            with self.lock:
                messages_to_remove = []
                for cached_message, receivers in self.message_receivers.items():
                    received_devices = set([peer[0] for peer in receivers])

                    # Check if both sets have the same values
                    if devices_to_check == received_devices:
                        messages_to_remove.append(cached_message)

                for message in messages_to_remove:
                    # Send a deleted message to 10.35.70.24:33340
                    deleted_file = message.split(": Delete ")[1].strip()
                    self.send_deleted_message("10.35.70.24", 33340, deleted_file, repetitions=20, interval=450)
                    
                    self.message_receivers.pop(message)
                    self.message_cache.remove(message)
                    print(f"Removed message from cache: {message}")


if __name__ == "__main__":
    # Define your host, port, and a list of known peers
    current_id = "Moon_Satellite"
    current_host = "10.35.70.24"
    current_port = 33342
    known_peers = [("10.35.70.12", 33343), ("10.35.70.28", 33344), ("10.35.70.42", 33345)]

    # Create a Peer instance
    peer = Peer(current_host, current_port, known_peers)

    # Start the check_and_remove_messages thread
    threading.Thread(target=peer.check_and_remove_messages).start()

    peer.start()
