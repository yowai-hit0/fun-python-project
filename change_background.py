# Import modules
import ctypes
import os
import psutil
import random

# Define constants
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 1
SPIF_SENDCHANGE = 2

# Define the path of the image file you want to use when your PC is charging
charging_image = "C:/Users/PC/Pictures/pic/charge.jpg"

# Define the path of the folder containing random images
random_images_folder = "C:/Users/PC/Pictures/pic/red/rand"


# Define a function to get a random image from a local folder
def get_random_local_image(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg', '.jfif'))]
    if image_files:
        random_image = os.path.join(folder_path, random.choice(image_files))
        return random_image
    else:
        return None


# Define a function to set the background image
def set_background_image(image_path):
    if os.path.isfile(image_path):
        image_path = image_path.replace("/", "\\")
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path,
                                                   SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
        print(f"Background image set to {image_path}")
    else:
        print(f"Image file not found: {image_path}")


# Check the battery status
current_status = psutil.sensors_battery().power_plugged

# Check if the current status is True (plugged in)
if current_status:
    set_background_image(charging_image)
else:
    # Get a random image from the local folder
    random_image = get_random_local_image(random_images_folder)

    # Check if the random image is not None
    if random_image:
        # Set the background image to the random image
        set_background_image(random_image)
    else:
        # Print a message if no random image is found
        print("No random image found in the folder.")
