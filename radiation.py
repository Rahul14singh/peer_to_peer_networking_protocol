import random
import time
import csv
import os
from datetime import datetime

# Weilong & Pradosh main contribution

def collect_radiation_data():
    LOW = 0.1
    HIGH = 0.4
    radiation_level = random.uniform(LOW, HIGH)
    #print(f"radiation_level: {radiation_level} μSv/h")
    return radiation_level

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass  # Directory already exists, ignore the error

def save_radiation_data(directory_to_write, timestamp, radiation, data_unit):
    # Determine the file name based on the elapsed time within the current hour
    elapsed_minutes = timestamp.minute
    file_name = f"radiation{15 * (elapsed_minutes // 15)}.csv"
    
    file_path = os.path.join(directory_to_write, file_name)
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Check if the file is empty, and if so, write the header
        if os.stat(file_path).st_size == 0:
            writer.writerow(["Timestamp", f"radiation_level({data_unit})"])

        writer.writerow([timestamp, radiation])


# Set the duration for the script to run (15 minutes)
duration = 15 * 60  # 15 minutes in seconds
start_time = time.time()
radiation_unit = "μSv/h"

while True:
    # Check if 15 minutes have passed
    if time.time() - start_time > duration:
        break

    # radiation reading
    radiation = collect_radiation_data()

    # Get the current timestamp
    current_timestamp = datetime.now()

    # Create directories for each day and hour
    day_directory = current_timestamp.strftime("%Y-%m-%d")
    hour_directory = current_timestamp.strftime("%H")
    directory_to_write = os.path.join("/users/pgrad/singhr6/group24/data", day_directory, hour_directory)
    create_directory_if_not_exists("/users/pgrad/singhr6/group24/data")
    create_directory_if_not_exists(os.path.join("/users/pgrad/singhr6/group24/data", day_directory))
    create_directory_if_not_exists(directory_to_write)
    
    # Save the radiation reading with timestamp to the CSV file
    save_radiation_data(directory_to_write, current_timestamp, radiation, radiation_unit)

    # Print the simulated radiation reading with timestamp (optional)
    print(f"{current_timestamp} - radiation: {radiation} {radiation_unit}")

    # Wait for 30 seconds before generating the next reading
    time.sleep(30)

# Print a message indicating the end of the script
print("Script completed after 15 minutes.")

