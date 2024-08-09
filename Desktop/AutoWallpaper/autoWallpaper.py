import ctypes
import os
import sys
import random
import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import getpass

SPI_SETDESKWALLPAPER = 20  # Specific call to Windows API to change background
PATH_IMAGES = f"C:\\Users\\{getpass.getuser()}\\Pictures\\Wallhaven Images"  # Set the path to where you want to store images

class Main:
    def __init__(self):
        self.path = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.path_images = os.path.join(self.path, PATH_IMAGES)
        self.backgrounds = []

        if not os.path.exists(self.path_images):
            os.makedirs(self.path_images)
            print(f"Directory '{self.path_images}' created.")
        else:
            print(f"Directory '{self.path_images}' already exists.")

        self.load_existing_images()

        self.get_latest_images(10)

        self.set_random_wallpaper()

    def load_existing_images(self):
        """Load existing images from the specified directory."""
        for root, dirs, files in os.walk(self.path_images):
            self.backgrounds = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg'))]

    def change_wallpaper(self, image_path):
        """Change the desktop wallpaper."""
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

    def download_image(self, url, name):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

        image_path = os.path.join(self.path_images, name)
        urllib.request.urlretrieve(url, image_path)
        
        print(f'Downloaded image [{url[-10:]}] from Wallhaven.CC')

        self.backgrounds.append(name)

    def get_latest_images(self, amount):
        """Retrieve the latest images from Wallhaven."""
        if 1 <= amount <= 20:
            url = 'https://wallhaven.cc'
            r = requests.get(url)
            count = 0
            soup = BeautifulSoup(r.text, 'html.parser')
            images = soup.find_all("img")
            url_list = []

            for image in images:
                if str(image['src']).startswith('https://th.wallhaven'):
                    url_list.append(str(image['src'])[-13:])
                    count += 1
                    print("Added: " + str(image['src'])[-13:])
                    if count >= amount:
                        break

            for image in url_list:
                if image[3:] not in self.backgrounds:
                    try:
                        self.download_image(f'https://w.wallhaven.cc/full/{image[:2]}/wallhaven-{image[3:]}', image[3:])
                    except:
                        self.download_image(f'https://w.wallhaven.cc/full/{image[:2]}/wallhaven-{image[3:-4]}.png', image[3:-4] + '.png')
                else:
                    print("Image already in 'images'")
        else:
            print("Please stay within 1 and 20")

    def set_random_wallpaper(self):
        """Set a random image from the backgrounds as the desktop wallpaper."""
        if self.backgrounds:
            self.image_path = os.path.join(self.path_images, random.choice(self.backgrounds))
            print(f"Setting wallpaper: {self.image_path}")
            self.change_wallpaper(self.image_path)
        else:
            print("No images found to set as wallpaper.")

if __name__ == "__main__":
    application = Main()
