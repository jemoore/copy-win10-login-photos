# -*- coding: utf-8 -*-

import os
import datetime
from shutil import copyfile
from PIL import Image


APP_DATA = os.environ['LOCALAPPDATA']

ASSET_DIR = "{0}\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets".format(APP_DATA)

TEMP_DIR = os.environ['TEMP']

CUR_TIME = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

TEMP_ASSET_DIR = "{0}\\assets-{1}".format(TEMP_DIR, CUR_TIME)

WALLPAPER_DIR = "your-storage-dir-here"

def copy_assets():
    
    if( len(APP_DATA) == 0 or not os.path.isdir(APP_DATA) ):
        print("AppData directory does not exist: {0}".format(APP_DATA))
        return
    if(  not os.path.isdir(ASSET_DIR) ):
        print("Asset directory does not exist: {0}".format(ASSET_DIR))
        return
    if( not os.path.isdir(TEMP_DIR) ):
        print("Temp directory does not exist: {0}".format(TEMP_DIR))
        return
    
    try:
        os.mkdir(TEMP_ASSET_DIR)
    except OSError as e:
        print("Could not create temp asset directory: {0}".format(TEMP_ASSET_DIR))
        print(e.strerror)
        return;
    
    files = [ f for f in os.listdir(ASSET_DIR) if os.path.isfile(os.path.join(ASSET_DIR, f))]
    owned = [ f for f in os.listdir(WALLPAPER_DIR) if os.path.isfile(os.path.join(WALLPAPER_DIR, f)) ]
    
    files_to_remove = []
    
    for file in files:
        src = os.path.join(ASSET_DIR, file)
        jpg_file = file + ".jpg"
        dest = os.path.join(TEMP_ASSET_DIR, jpg_file)

        copyfile( src, dest )
        
        try:
            image = Image.open(dest)
            image.load()
            width, height = image.size
            
            # if not screen sized or already previously copied, delete it
            if( width < 1920 or height < 1080 or jpg_file in owned ):
                files_to_remove.append(dest)

        except:
            files_to_remove.append(dest)
            continue
        
    for file in files_to_remove:
        os.remove(file)
        
    
if __name__ == "__main__":
    copy_assets()
    