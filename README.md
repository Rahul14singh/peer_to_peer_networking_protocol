# Peer-to-Peer Networking Protocol 

Peer to Peer Networking Protocol to communicate between Raspberry Pi's.

(Use Case) Communication between different Satellites around Mars and Earth and sending sensor data collected by all peers securely through sensors back to Earth.


List of Peers:
1. Curiosity Rover
2. Mars Rover
3. Mars Lander
4. Mars satellite
5. Moon satellite
6. Earth(system)


## Setup the env by running the bash script run.sh first

```bash
$ source run.sh
```

## To Test RSA & Encryption 

```bash
peer_receiver_landerModule_rsademo.py

peer_sender_marsRover_rsademo.py
```

These are the files we will need to check for RSA and Encryption.

Run peer_receiver_landerModule_rsademo.py where you want to listen preferably on IP_MOON_SATELLITE.

Then run peer_sender_marsRover_rsademo.py and it will send the last 5 hours of data to the receiver with encryption and decryption

> **Note**: Keep the *.pem files and data_test directory in same directory as the codes 


## To test Broadcast deletion the whole deletion channel

> **Note**: Update IPs in the code if not using PIs as mentioned below to run these:

> **Note**: At first start listening on all these PIs and then press enter from curiosity rover to earth to connect to peers this can be made automatic in a later version

> **Note**: Keep the data_test directory in the same directory as the codes 

peer_broadcast_curiosityRover.py  
PI is IP_CURIOSITY_ROVER run these on this PI with the order as mentioned from left to right

peer_broadcast_marsRover.py     
PI is IP_MARS_ROVER run these on this PI with the order as mentioned from left to right

peer_broadcast_landerModule.py  
PI is IP_LANDER_MODULE run these on this PI with the order as mentioned from left to right

peer_broadcast_marsSatellite.py
PI is IP_MARS_SATELLITE run these on this PI with the order as mentioned from left to right

peer_broadcast_moonSatellite.py
PI is IP_MOON_SATELLITE run these on this PI with the order as mentioned from left to right

peer_broadcast_earth.py           
PI is IP_EARTH run these on this PI with the order as mentioned from left to right

## To Test and simulate data generation and to test sending and receiving the whole data over the channel peer-to-peer connection

> **Note**: Update IPs in the code if not using PIs as mentioned below to run these

> **Note**: Keep the data_test directory in same directory as the codes 

if you go to these pi just do a crontab -e and add the lines from the-crontab file given in the bundle to make everything start working automatically   

launcher_curiosityRover.py peer_receiver_curiosityRover.py  peer_sender_curiosityRover.py 
PI is IP_CURIOSITY_ROVER run these on this PI with the order as mentioned from left to right

launcher_marsRover.py peer_receiver_marsRover.py  peer_sender_marsRover.py 
PI is IP_MARS_ROVER run these on this PI with the order as mentioned from left to right

launcher_landerModule.py peer_receiver_landerModule.py  peer_sender_landerModule.py 
PI is IP_LANDER_MODULE run these on this PI with the order as mentioned from left to right

launcher_marsSatellite.py peer_receiver_marsSatellite.py  peer_sender_marsSatellite.py 
PI is IP_MARS_SATELLITE run these on this PI with the order as mentioned from left to right

launcher_moonSatellite.py peer_receiver_moonSatellite.py  peer_sender_moonSatellite.py 
PI is IP_MOON_SATELLITE run these on this PI with the order as mentioned from left to right

peer_receiver_earth.py 
PI is IP_EARTH run these on this PI with the order as mentioned from left to right

the launcher_* scripts will start creating dummy data and peer_sender_* scripts will start sending it and the peer_receiver_* scripts will start receiving the data on all peers.
