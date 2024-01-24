# Peer-to-Peer Networking Protocol 

Robust Inter-Planetary Communication Network

This project implements a peer-to-peer (P2P) networking protocol designed to facilitate secure and efficient data exchange between various satellites orbiting Mars and Earth. The network comprises a diverse set of nodes representing different spacecraft:

List of Peers:

1. Curiosity Rover
2. Mars Rover
3. Mars Lander
4. Mars satellite
5. Moon satellite
6. Earth(system)


## Setting Up the Environment

To establish the communication environment, execute the provided bash script run.sh to initialize the necessary configurations:

```bash
$ source run.sh
```


### Testing RSA Encryption and Decryption

Verify the implementation of RSA encryption and decryption modules using the following scripts:

```bash
peer_receiver_landerModule_rsademo.py

peer_sender_marsRover_rsademo.py
```

Run peer_receiver_landerModule_rsademo.py on the desired listening device, preferably on the IP address of the Moon Satellite. Then, execute peer_sender_marsRover_rsademo.py to transmit the last 5 hours of data to the receiver, ensuring secure encryption and decryption.

> **Note**: Ensure that the *.pem files and the data_test directory are located in the same directory as the scripts.


### Testing Broadcast Channel Deletion 

Data deletion from each peer occurs through broadcasting once successful verification of reception at Earth is confirmed.

To test the deletion of data from the broadcast channel:

a). Update the IP addresses in the scripts to reflect the actual network configuration (if not using Raspberry Pis).
b). Initially, initiate listening on all devices using the provided scripts.
c). From the Curiosity Rover, press enter to connect to the other peers. This can be automated in future versions.
d). Keep the data_test directory in the same directory as the scripts.

Following are the broadcasting scripts to be deployed on every peer (in this case Raspberry Pi) to able to communicate with each other:

1. peer_broadcast_curiosityRover.py  
2. peer_broadcast_marsRover.py     
3. peer_broadcast_landerModule.py  
4. peer_broadcast_marsSatellite.py
5. peer_broadcast_moonSatellite.py
6. peer_broadcast_earth.py           

### Testing Data Generation and Transmission

To simulate data generation and test sending and receiving data over the P2P channel:

a). Update the IP addresses in the scripts to match your network configuration (if not using Raspberry Pis).
b). Keep the data_test directory in the same directory as the scripts. 

Following are the scripts to be deployed on separate peers (in this case Raspberry Pi) to start the communication in the system:

1. launcher_curiosityRover.py  peer_receiver_curiosityRover.py   peer_sender_curiosityRover.py 
2. launcher_marsRover.py  peer_receiver_marsRover.py   peer_sender_marsRover.py 
3. launcher_landerModule.py  peer_receiver_landerModule.py   peer_sender_landerModule.py 
4. launcher_marsSatellite.py  peer_receiver_marsSatellite.py   peer_sender_marsSatellite.py 
5. launcher_moonSatellite.py  peer_receiver_moonSatellite.py   peer_sender_moonSatellite.py 
6. peer_receiver_earth.py 

The launcher_* scripts will generate dummy data, the peer_sender_* scripts will transmit the data, and the peer_receiver_* scripts will capture the data on all peers.
