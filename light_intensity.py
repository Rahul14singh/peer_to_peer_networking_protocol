import random
import time
import csv
import os
from datetime import datetime

# Weilong & Pradosh main contribution

def simulate_light_intensity():
    light_intensity = random.uniform(0, 100)  # Adjust the range as needed
    return light_intensity

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass  # Directory already exists, ignore the error

def save_light_data(directory, timestamp, light_intensity):
    # Determine the file name based on the elapsed time within the current hour
    elapsed_minutes = timestamp.minute
    file_name = f"light_intensity{15 * (elapsed_minutes // 15)}.csv"
    
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if os.stat(file_path).st_size == 0:
            writer.writerow(["Timestamp", "Light Intensity (lux)"])
        writer.writerow([timestamp, light_intensity])

# Set the duration for the script to run (15 minutes)
duration =  15 * 60 # 15 minutes in seconds
start_time = time.time()

while True:
    # Check if 15 minutes have passed
    if time.time() - start_time > duration:
        break

    # Get the current timestamp
    current_timestamp = datetime.now()

    # Create directories for each day and hour
    day_directory = current_timestamp.strftime("%Y-%m-%d")
    hour_directory = current_timestamp.strftime("%H")
    directory_to_write = os.path.join("/users/pgrad/singhr6/group24/data", day_directory, hour_directory)
    create_directory_if_not_exists("/users/pgrad/singhr6/group24/data")
    create_directory_if_not_exists(os.path.join("/users/pgrad/singhr6/group24/data", day_directory))
    create_directory_if_not_exists(directory_to_write)

    # Generate simulated light intensity reading
    light_intensity = simulate_light_intensity()

    # Save the simulated light intensity reading with timestamp to the CSV file
    save_light_data(directory_to_write, current_timestamp, light_intensity)

    # Print the simulated light intensity reading with timestamp (optional)
    print(f"{current_timestamp} - Simulated Light Intensity: {light_intensity} lux")

    # Wait for 30 seconds before generating the next reading
    time.sleep(30)

# Print a message indicating the end of the script
print("Script completed after 15 minutes.")

