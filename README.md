# Peer to Peer Networking Protocol 

Peer to Peer Networking Protocol to communicate between Raspberry Pi's (Use Case) Communication between different Satellites around Mars and Earth and sending sensor data securely from sensors to Earth.

Curiosity Rover
Pi- IP_CURIOSITY_ROVER 
Port- PORT_CURIOSITY_ROVER
Deletion port-PORT_CURIOSITY_ROVER

Mars Rover
Pi-IP_MARS_ROVER
Port-PORT_MARS_ROVER 
Deletion port-PORT_MARS_ROVER

Mars Lander
Pi-IP_MARS_LANDER
Port-PORT_MARS_LANDER
Deletion port-PORT_MARS_LANDER

Mars satellite
Pi-IP_MARS_SATELLITE
Port-PORT_MARS_SATELLITE
Deletion port-PORT_MARS_SATELLITE

Moon satellite
Pi-IP_MOON_SATELLITE
Port-PORT_MOON_SATELLITE
Deletion port-PORT_MOON_SATELLITE

Earth(system)
Pi-IP_EARTH
Port-PORT_EARTH
Deletion port-PORT_EARTH



# Setup the env by running the bash script run.sh first

$ source run.sh





# To Test RSA & Encryption 

peer_receiver_landerModule_rsademo.py

peer_sender_marsRover_rsademo.py


These are the files we will need to check RSA and Encryption

Run peer_receiver_landerModule_rsademo.py where you want to listen preferably on IP_MOON_SATELLITE if we do not want to make changes on peer_sender_marsRover_rsademo.py or else change the ip accordingly on sender file

Then run peer_sender_marsRover_rsademo.py and it will send last 5 hours of data to the reciver with encryption and decryption

#Note: Keep the *.pem files and data_test directory in same directory as the codes 






# To test Broadcast deletion the whole deletion channel

#Note: Update IPs in the code if not using PIs as mentioned below to run these (Did not got time to make these genric with routing table)

#Note: At first start listning on all these PIs and then press enter from curiosityRover to earth in order to connect to peers this can be made automatic i.e. keep trying to connect to peers but did not got chance to work on this 

#Note: Keep the data_test directory in same directory as the codes 

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
PI is IP_MOON_SATELLITE run these on this PI with the order as mentioned from left to right








# To Test data generation and sending receiving the whole data channel 

#Note: Update IPs in the code if not using PIs as mentioned below to run these (Did not got time to make these genric with routing table)

#Note: Keep the data_test directory in same directory as the codes 

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
PI is IP_MOON_SATELLITE run these on this PI with the order as mentioned from left to right

launcher will start creating dummy data sender will start sending it and reciver will start recieveing on the peers.
