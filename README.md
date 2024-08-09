# Wallhaven Autodownloader
A script that fetches top 10 images on Wallhaven and sets it to your desktop wallpaper.

## Setup
Download "autoWallpaper.py" and put it wherever you want. If you want to automate it, just remember the path and read "Automation".
I recommend the user directory under Pictures.

### Image Location
By default, images will be saved to `user/Pictures/Wallhaven Images`, but you can change this.
Just modify the variable, `PATH_IMAGES`, to your desired location. Note that you need to put double backslash between directories.

## Automation
To automate on startup on Windows, do the following:

1. Copy the path of the program.
2. Press Windows + R and run `shell:startup`.
3. In the folder, create a .txt file and run following code:
4. python "[PATH_TO_SCRIPT]"
   Note that only one backslash is required here.
5. Save the file as `wallhaven.bat`

The script will now run every time you start your computer.



