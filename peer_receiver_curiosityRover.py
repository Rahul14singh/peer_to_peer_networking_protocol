import socket
import threading
import csv
import json
import argparse
import os
import ast

# Rahul & Rasika & Weilong & Pradosh main contribution

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass # Do nothing

def save_data_csv(peer_name, sensor_name, date, hour, data):
    path_to_save = os.path.join("/users/pgrad/zhangj20/group24/data", peer_name, date, hour)
    create_directory_if_not_exists(path_to_save)
    data_dict = ast.literal_eval(data)
    with open(os.path.join(path_to_save, f"{peer_name}_{sensor_name}.csv"), 'w', newline='') as csvfile:
        # Create a CSV writer object
        csvwriter = csv.writer(csvfile)

        # Write the header row
        csvwriter.writerow(data_dict.keys())

        # Find the maximum number of values among all keys
        max_values = max(len(values) for values in data_dict.values())

        # Write the data rows
        for i in range(max_values):
            # Create a list to store the values for this row
            row_data = []
            for key in data_dict.keys():
                # If the key has fewer values, use None for missing data
                value = data_dict[key][i] if i < len(data_dict[key]) else None
                row_data.append(value)
            csvwriter.writerow(row_data)



def check_message_correctness(input_data):
    # Count occurrences of specified substrings
    opening_brace_count = input_data.count('{')
    closing_brace_count = input_data.count('}')
    colon_brace_count = input_data.count(':{')
    
    # Check conditions
    if opening_brace_count == 1 and closing_brace_count == 1 and colon_brace_count == 1:
        return True
    else:
        return False

def get_data(input_data):
    data_dict = {}
    peer_name = input_data.split(":")[0]
    sensor_name = input_data.split(":")[1]
    devices = ["Curiosity_Rover", "Mars_Rover", "Lander_Module", "Mars_Satellite", "Moon_Satellite", "Earth"]
    for device in devices:
        if device in sensor_name:
            peer_name = device
            sensor_name = sensor_name.replace(device + "_", "")
    message = "{" + input_data.split(":{")[1]
    temp = (message.split('Timestamp": ["')[1]).split('",')[0]
    date = temp.split(" ")[0]
    hour = temp.split(" ")[1].split(":")[0]
    data_dict['peer_name'] = peer_name
    data_dict['sensor_name'] = sensor_name
    data_dict['message'] = message
    data_dict['date'] = date
    data_dict['hour'] = hour
    return data_dict

def receive_data(sock):
    data = sock.recv(90000)
    message = data.decode('utf-8')
    return message

def handle_peer(peer_socket, addr):
    print(f"Accepted connection from {addr}")
    with peer_socket as sock:
        while True:
            try:
                message = receive_data(sock)
                print(f"Received message: {message}")
                if not message:
                    break

                if check_message_correctness(message):
                    data_dict = get_data(message)
                    peer_name, sensor_name = data_dict['peer_name'], data_dict['sensor_name']
                    date, hour = data_dict['date'], data_dict['hour']
                    save_data_csv(peer_name, sensor_name, date, hour, data_dict['message'])

                    response_message = f"Peer received your message: {message}"
                    sock.send(response_message.encode('utf-8'))
                else:
                    response_message = f"Peer received an invalid message: {message}"
                    sock.send(response_message.encode('utf-8'))

            except ConnectionResetError:
                print(f"Connection forcibly closed by {addr}")
                break
            except Exception as e:
                print(f"An exception occurred: {e}")
                break

def start_peer(host, port):
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    peer_socket.bind((host, port))
    peer_socket.listen()

    print(f"Peer is listening for connections on {host}:{port}")

    while True:
        peer_client_socket, addr = peer_socket.accept()
        peer_handler = threading.Thread(target=handle_peer, args=(peer_client_socket, addr))
        peer_handler.daemon = True
        peer_handler.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Peer Receiver Server")
    parser.add_argument("--host", default='0.0.0.0', help="Host IP address")
    parser.add_argument("--port", type=int, default=33337, help="Port number")
    args = parser.parse_args()

    start_peer(args.host, args.port)
