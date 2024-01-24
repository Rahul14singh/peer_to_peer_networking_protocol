#!/bin/bash

# Create data_test directory if it doesn't exist
mkdir -p data_test

# Get current date and time
current_date=$(date +"%Y-%m-%d")
current_hour=$(date +"%H")

# Create directories based on the current date and hour
mkdir -p "data_test/$current_date"
mkdir -p "data_test/$current_date/$current_hour"

# Copy files from the 'data' directory to the current hour directory
cp -r data/* "data_test/$current_date/$current_hour/"

# Create logs directory if it doesn't exist
mkdir -p logs

# Get the current directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "##### Add the Below on PI 12 and install on crontab by crontab -e" > the-crontab

echo "#Run the scripts to generate the sensor data" >> the-crontab
echo "*/15 * * * * /usr/bin/python3 ${SCRIPT_DIR}/launcher_curiosityRover.py >> ${SCRIPT_DIR}/logs/launcher_$(date +\%Y\%m\%d\%H\%M\%S).log 2>&1" >> the-crontab

echo "#Run the script to send data to the server every 15 minutes" >> the-crontab
echo "*/15 * * * * /usr/bin/python3 ${SCRIPT_DIR}/peer_sender_curiosityRover.py >> ${SCRIPT_DIR}/logs/peer_sender_$(date +\%Y\%m\%d\%H\%M\%S).log 2>&1" >> the-crontab

echo "#Run the script to receive data" >> the-crontab
echo "*/14 * * * * /usr/bin/python3 ${SCRIPT_DIR}/peer_receiver_curiosityRover.py" >> the-crontab


echo " " >> the-crontab
echo " " >> the-crontab


echo "##### Add the Below on PI 28 and install on crontab by crontab -e" >> the-crontab

echo "#Run the scripts to generate the sensor data" >> the-crontab
echo "*/15 * * * * /usr/bin/python3 ${SCRIPT_DIR}/launcher_marsRover.py >> ${SCRIPT_DIR}/logs/launcher_$(date +\%Y\%m\%d\%H\%M\%S).log 2>&1" >> the-crontab

echo "#Run the script to send data to the server every 15 minutes" >> the-crontab
echo "*/15 * * * * /usr/bin/python3 ${SCRIPT_DIR}/peer_sender_marsRover.py >> ${SCRIPT_DIR}/logs/peer_sender_$(date +\%Y\%m\%d\%H\%M\%S).log 2>&1" >> the-crontab

echo "#Run the script to receive data" >> the-crontab
echo "*/14 * * * * /usr/bin/python3 ${SCRIPT_DIR}/peer_receiver_marsRover.py" >> the-crontab


echo " " >> the-crontab
echo " " >> the-crontab


echo "##### Add the Below on PI 42 and install on crontab by crontab -e" >> the-crontab

echo "#Run the scripts to generate the sensor data" >> the-crontab
echo "*/15 * * * * /usr/bin/python3 ${SCRIPT_DIR}/launcher_landerModule.py >> ${SCRIPT_DIR}/logs/launcher_$(date +\%Y\%m\%d\%H\%M\%S).log 2>&1" >> the-crontab

echo "#Run the script to send data to the server every 15 minutes" >> the-crontab
echo "*/15 * * * * /usr/bin/python3 ${SCRIPT_DIR}/peer_sender_landerModule.py >> ${SCRIPT_DIR}/logs/peer_sender_$(date +\%Y\%m\%d\%H\%M\%S).log 2>&1" >> the-crontab

echo "#Run the script to receive data" >> the-crontab
echo "*/14 * * * * /usr/bin/python3 ${SCRIPT_DIR}/peer_receiver_landerModule.py" >> the-crontab


echo " " >> the-crontab
echo " " >> the-crontab


echo "##### Add the Below on PI 31 and install on crontab by crontab -e" >> the-crontab

echo "#Run the scripts to generate the sensor data" >> the-crontab
echo "*/15 * * * * /usr/bin/python3 ${SCRIPT_DIR}/launcher_marsSatellite.py >> ${SCRIPT_DIR}/logs/launcher_$(date +\%Y\%m\%d\%H\%M\%S).log 2>&1" >> the-crontab

echo "#Run the script to send data to the server every 15 minutes" >> the-crontab
echo "*/15 * * * * /usr/bin/python3 ${SCRIPT_DIR}/peer_sender_marsSatellite.py >> ${SCRIPT_DIR}/logs/peer_sender_$(date +\%Y\%m\%d\%H\%M\%S).log 2>&1" >> the-crontab

echo "#Run the script to receive data" >> the-crontab
echo "*/14 * * * * /usr/bin/python3 ${SCRIPT_DIR}/peer_receiver_marsSatellite.py" >> the-crontab


echo " " >> the-crontab
echo " " >> the-crontab


echo "##### Add the Below on PI 24 and install on crontab by crontab -e" >> the-crontab

echo "#Run the scripts to generate the sensor data" >> the-crontab
echo "*/15 * * * * /usr/bin/python3 ${SCRIPT_DIR}/launcher_moonSatellite.py >> ${SCRIPT_DIR}/logs/launcher_$(date +\%Y\%m\%d\%H\%M\%S).log 2>&1" >> the-crontab

echo "#Run the script to send data to the server every 15 minutes" >> the-crontab
echo "*/15 * * * * /usr/bin/python3 ${SCRIPT_DIR}/peer_sender_moonSatellite.py >> ${SCRIPT_DIR}/logs/peer_sender_$(date +\%Y\%m\%d\%H\%M\%S).log 2>&1" >> the-crontab

echo "#Run the script to receive data" >> the-crontab
echo "*/14 * * * * /usr/bin/python3 ${SCRIPT_DIR}/peer_receiver_moonSatellite.py" >> the-crontab

echo "# Earth on PI 24" >> the-crontab
echo "#Run the script to receive data" >> the-crontab
echo "*/14 * * * * /usr/bin/python3 ${SCRIPT_DIR}/peer_receiver_earth.py" >> the-crontab

# Update paths in .py files
for FILE in ${SCRIPT_DIR}/*.py; do
    # Check if the file exists and is a regular file
    if [ -f "${FILE}" ]; then
        # Replace /users/pgrad/*/group24/ with ${SCRIPT_DIR}
        sed -i "s|/users/pgrad/[^/]*/group24/|${SCRIPT_DIR}/|g" "${FILE}"
    fi
done
