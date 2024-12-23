# Import modules
import ctypes
import os
import psutil
import requests
import time
import random

# Define constants
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 1
SPIF_SENDCHANGE = 2

# Define the path of the image file you want to use when you charge your PC
charging_image = "C:/Users/PC/Pictures/pic/charge.jpg"
not_charging_folder = "C:/Users/PC/Pictures/pic/red/rand"
# Define a function to get a random image from the web
def get_random_image():
    # Get a random image URL from Unsplash
    url = "https://source.unsplash.com/random"
    # Send a GET request to the URL
    response = requests.get(url)
    # Check if the response is successful
    if response.status_code == 200:
        # Get the content of the response as bytes
        image_data = response.content
        # Save the image data to a temporary file
        image_file = "temp.jpg"
        with open(image_file, "wb") as f:
            f.write(image_data)
        # Return the path of the image file
        return os.path.abspath(image_file)
    else:
        # Return None if the response is not successful
        return None

def get_random_image_from_folder(folder_path):
    # Check if the folder exists
    if os.path.isdir(folder_path):
        # Get a list of all files in the folder
        files = os.listdir(folder_path)
        # Filter out non-image files (you can customize this based on your image types)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        # Check if there are any image files in the folder
        if image_files:
            # Select a random image from the list
            selected_image = random.choice(image_files)
            # Return the full path of the selected image
            return os.path.join(folder_path, selected_image)
    # Return None if the folder or no suitable images are found
    return None

# Define a function to set the background image
def set_background_image(image_path):
    # Check if the image file exists
    if os.path.isfile(image_path):
        # Convert the image path to a Windows-friendly format
        image_path = image_path.replace("/", "\\")
        # Set the image as the background using the Windows API
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
        # Print a message to indicate success
        print(f"Background image set to {image_path}")
    else:
        # Print a message to indicate failure
        print(f"Image file not found: {image_path}")

# Define a function to check the battery status
def check_battery_status():
    # Get the battery information using the psutil module
    battery = psutil.sensors_battery()
    # Check if the battery is plugged in or not
    plugged = battery.power_plugged
    # Return the plugged status as a boolean
    return plugged

# Define a variable to store the previous battery status
previous_status = None

# Define a loop to run the script continuously
while True:
    # Get the current battery status
    current_status = check_battery_status()
    # Check if the current status is different from the previous status
    if current_status != previous_status:
        # Check if the current status is True (plugged in)
        if current_status:
            # Set the background image to the charging image
            set_background_image(charging_image)
        else:
            # Get a random image from the web
            random_image = get_random_image_from_folder(not_charging_folder)
            # Check if the random image is not None
            if random_image:
                # Set the background image to the random image
                set_background_image(random_image)
        # Update the previous status to the current status
        previous_status = current_status
    # Wait for 10 seconds before checking again
    time.sleep(3)
