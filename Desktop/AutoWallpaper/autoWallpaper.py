import ctypes
import os
import sys
import random
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

SPI_SETDESKWALLPAPER = 20 # SPECIFIC CALL TO WINDOWS API TO CHANGE BACKGROUND
PATH_IMAGES = "C:\\Users\\Mark\\Desktop\\images" # SET YOUR PATH TO WHERE YOU WANT TO STORE IMAGES

def change_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

def download_image(url, name):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    urllib.request.urlretrieve(url, PATH_IMAGES + '\\' + name)
    
    print(f'Downloaded image [{url[-10:]}] from Wallhaven.CC')

def get_latest_images(amount):
    if 1 <= amount and amount <= 20:
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
                if count > amount:
                    break
        for image in url_list:

            if image[3:] not in os.listdir(PATH_IMAGES):
                try:
                    download_image(f'https://w.wallhaven.cc/full/{image[:2]}/wallhaven-{image[3:]}', image[3:])
                except:
                    download_image(f'https://w.wallhaven.cc/full/{image[:2]}/wallhaven-{image[3:-4]}.png', image[3:-4] + '.png')
            else:
                print("Image already in 'images'")
    else:
        print("Please stay within 1 and 20")


class Main:
    def __init__(self):
        self.path = os.path.abspath(os.path.dirname(sys.argv[0]))
        for root, dirs, files in os.walk(PATH_IMAGES):
            self.backgrounds = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg'))]

        print(self.backgrounds)
        
        
        get_latest_images(10)

        try:
            self.image_path = os.path.join(PATH_IMAGES, random.choice(self.backgrounds))
        except:
            self.image_path = os.path.join(PATH_IMAGES, self.backgrounds[0])
        print(self.image_path)

        change_wallpaper(self.image_path)

application = Main()
