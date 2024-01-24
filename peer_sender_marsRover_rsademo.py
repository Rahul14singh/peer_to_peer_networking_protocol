import socket
import csv
import glob
import json
import argparse
import os
from datetime import datetime, timedelta
import ssl
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import binascii

# Rasika Burde & Rahul Singh main contribution

def connect_to_peer(host, port):
    try:
        peer_socket = socket.create_connection((host, port))
        peer_ssl_socket = ssl.wrap_socket(peer_socket, ssl_version=ssl.PROTOCOL_TLSv1_2, certfile='cert.pem', keyfile='key_no_passphrase.pem', server_side=False, cert_reqs=ssl.CERT_NONE, suppress_ragged_eofs=True)
        return peer_ssl_socket
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    except socket.error as e:
        print(f"Connection error: {e}")
        return None

def disconnect_from_peer(peer_socket):
    """Disconnect from the peer server."""
    peer_socket.close()

def read_csv_file(filepath):
    """Read data from a CSV file and return it as a dictionary."""
    data = []
    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)

        sublists = [[] for _ in headers]
        for row in csv_reader:
            for i in range(len(headers)):
                sublists[i].append(row[i])

        data_dict = {}
        for i in range(len(headers)):
            data_dict[headers[i]] = sublists[i]
    return data_dict

def load_private_key_with_passphrase(key_path, passphrase=None):
    with open(key_path, 'r') as file:
        private_key = RSA.import_key(file.read(), passphrase=passphrase)
    return private_key

def rsa_decrypt(encrypted_message, private_key):
    # Convert the hex representation back to bytes
    final_message = binascii.unhexlify(encrypted_message)

    # Extract the encrypted symmetric key, tag, and ciphertext
    encrypted_symmetric_key = final_message[:private_key.size_in_bytes()]
    tag = final_message[private_key.size_in_bytes():private_key.size_in_bytes() + 16]  # Assuming 16 bytes for the tag
    ciphertext = final_message[private_key.size_in_bytes() + 16:]

    # Decrypt the symmetric key with RSA
    cipher_rsa = PKCS1_OAEP.new(private_key)
    symmetric_key = cipher_rsa.decrypt(encrypted_symmetric_key)

    # Decrypt the actual data with the symmetric key using AES
    cipher_aes = AES.new(symmetric_key, AES.MODE_EAX, nonce=b'unique_nonce')  # Set a unique nonce value
    decrypted_text = cipher_aes.decrypt_and_verify(ciphertext, tag)

    return decrypted_text.decode('utf-8')

def rsa_encrypt(message, public_key):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    symmetric_key = os.urandom(16)

    # Encrypt the symmetric key with RSA
    encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)

    # Encrypt the actual data with the symmetric key using AES in EAX mode
    cipher_aes = AES.new(symmetric_key, AES.MODE_EAX, nonce=b'unique_nonce')
    ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode())

    # Combine the encrypted symmetric key, tag, and ciphertext
    final_message = encrypted_symmetric_key + tag + ciphertext

    # Optionally, convert the final message to hexadecimal representation
    hex_final_message = binascii.hexlify(final_message).decode('utf-8')

    return hex_final_message

def send_peer_data(peer_socket, peer_id, filename, data_dict, public_key, private_key):
    """Send data to the peer server."""
    try:
        if data_dict:
            message = f"{peer_id}:{filename.split('.csv')[0]}:{json.dumps(data_dict)}"

            encrypted_message = rsa_encrypt(message, public_key)
            print("Encrypted Message is: " + encrypted_message)
            encrypted_message = encrypted_message.encode('utf-8')
            peer_socket.send(encrypted_message)

            # Wait for a response if needed
            response = peer_socket.recv(90000)
            print(f"Peer response: {response}")
    except socket.error as e:
        print(f"Socket error: {e}")
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")

def main(peer_ip_ports, peer_id, public_key_path, private_key_path, passphrase):

    # Load the public key
    with open(public_key_path, 'r') as file:
        public_key = RSA.import_key(file.read())

    # Load the private key with passphrase
    private_key = load_private_key_with_passphrase(private_key_path, passphrase)

    """Main function to connect to the peer and send data."""
    try:
        for i in range(1, 6):
            current_datetime = datetime.now()
            previous_datetime = current_datetime - timedelta(hours=i)
            current_date = previous_datetime.strftime("%Y-%m-%d")
            current_hour = previous_datetime.strftime("%H")
            
            for peer_ip, port in peer_ip_ports:
                csv_files = glob.glob(os.path.join("/users/pgrad/srivastp/group24/data_test", current_date, current_hour, "*.csv"))
                if csv_files:
                    for csv_file in csv_files:
                        # Connect to the peer server for each file
                        peer_socket = connect_to_peer(peer_ip, port)
                        if peer_socket:
                            filename = csv_file.split('/')[-1]
                            data = read_csv_file(csv_file)
                            send_peer_data(peer_socket, peer_id, filename, data, public_key, private_key)

                            # Disconnect from the peer server after each file
                            disconnect_from_peer(peer_socket)
                else:
                    print("No CSV files found for Date: " + current_date + " Hour: " + current_hour)

                csv_files = glob.glob(os.path.join("/users/pgrad/srivastp/group24/data_test/Curiosity_Rover", current_date, current_hour, "*.csv"))

                if csv_files:
                    for csv_file in csv_files:
                        # Connect to the peer server for each file
                        peer_socket = connect_to_peer(peer_ip, port)
                        if peer_socket:
                            filename = csv_file.split('/')[-1]
                            data = read_csv_file(csv_file)
                            send_peer_data(peer_socket, peer_id, filename, data, public_key, private_key)

                            # Disconnect from the peer server after each file
                            disconnect_from_peer(peer_socket)
                else:
                    print("No CSV files found for Curiosity_Rover Date: " + current_date + " Hour: " + current_hour)
            
                csv_files = glob.glob(os.path.join("/users/pgrad/srivastp/group24/data_test/Mars_Rover", current_date, current_hour, "*.csv"))

                if csv_files:
                    for csv_file in csv_files:
                        # Connect to the peer server for each file
                        peer_socket = connect_to_peer(peer_ip, port)
                        if peer_socket:
                            filename = csv_file.split('/')[-1]
                            data = read_csv_file(csv_file)
                            send_peer_data(peer_socket, peer_id, filename, data, public_key, private_key)

                            # Disconnect from the peer server after each file
                            disconnect_from_peer(peer_socket)
                else:
                    print("No CSV files found for Mars_Rover Date: " + current_date + " Hour: " + current_hour)
            
                csv_files = glob.glob(os.path.join("/users/pgrad/srivastp/group24/data_test/Lander_Module", current_date, current_hour, "*.csv"))

                if csv_files:
                    for csv_file in csv_files:
                        # Connect to the peer server for each file
                        peer_socket = connect_to_peer(peer_ip, port)
                        if peer_socket:
                            filename = csv_file.split('/')[-1]
                            data = read_csv_file(csv_file)
                            send_peer_data(peer_socket, peer_id, filename, data, public_key, private_key)

                            # Disconnect from the peer server after each file
                            disconnect_from_peer(peer_socket)
                else:
                    print("No CSV files found for Lander_Module Date: " + current_date + " Hour: " + current_hour)
            
                csv_files = glob.glob(os.path.join("/users/pgrad/srivastp/group24/data_test/Mars_Satellite", current_date, current_hour, "*.csv"))

                if csv_files:
                    for csv_file in csv_files:
                        # Connect to the peer server for each file
                        peer_socket = connect_to_peer(peer_ip, port)
                        if peer_socket:
                            filename = csv_file.split('/')[-1]
                            data = read_csv_file(csv_file)
                            send_peer_data(peer_socket, peer_id, filename, data, public_key, private_key)

                            # Disconnect from the peer server after each file
                            disconnect_from_peer(peer_socket)
                else:
                    print("No CSV files found for Mars_Satellite Date: " + current_date + " Hour: " + current_hour)
            
                csv_files = glob.glob(os.path.join("/users/pgrad/srivastp/group24/data_test/Moon_Satellite", current_date, current_hour, "*.csv"))

                if csv_files:
                    for csv_file in csv_files:
                        # Connect to the peer server for each file
                        peer_socket = connect_to_peer(peer_ip, port)
                        if peer_socket:
                            filename = csv_file.split('/')[-1]
                            data = read_csv_file(csv_file)
                            send_peer_data(peer_socket, peer_id, filename, data, public_key, private_key)

                            # Disconnect from the peer server after each file
                            disconnect_from_peer(peer_socket)
                else:
                    print("No CSV files found for Moon_Satellite Date: " + current_date + " Hour: " + current_hour)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send data to a peer.")
    parser.add_argument("--peer_ip_ports", nargs='+', default=[('10.35.70.24:33354')], help="List of tuples containing peer IP addresses and ports")
    parser.add_argument("--peer_id", default='Mars_Rover', help="Unique identifier for this peer")
    args = parser.parse_args()

    # Parse the string representations of tuples and convert port numbers to integers
    args.peer_ip_ports = [(ip, int(port)) for ip, port in (pair.split(':') for pair in args.peer_ip_ports)]
    
    main(args.peer_ip_ports, args.peer_id, "cert.pem", "key_no_passphrase.pem", "scalable")

