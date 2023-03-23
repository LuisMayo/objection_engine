from .loading import load_music_data 
from collections import Counter
import os
import requests
import zipfile
import shutil
import json
from toml import dump

def ensure_assets_are_available():
    if not os.path.exists('assets') or not os.listdir('assets'):
        download_assets()
        os.remove('assets.zip')
    else:
        # This is in case there are only some missing assets that have been added in updates
        detect_old_assets_format()

def download_assets():
    print('Assets not present. Downloading them')
    response = requests.get('https://dl.luismayo.com/assetsv4.zip')
    with open('assets.zip', 'wb') as file:
        file.write(response.content)
    with zipfile.ZipFile('assets.zip', 'r') as zip_ref:
        zip_ref.extractall('assets')

def detect_old_assets_format():
    if os.path.exists('./Sprites-phoenix'):
        print("Old assets format detected. Moving assets folder to assets_old")
        os.rename("./assets", "./assets_old")
        download_assets()
        print("Migrating music (if any) to the new assets folder with the new assets config")
        for music_folder in os.listdir("./assets_old/music"):
            if not os.path.exists("./assets/music/" + music_folder):
                print("Migrating " + music_folder)
                try:
                    shutil.copytree("./assets_old/music/" + music_folder, "./assets/music/" + music_folder)
                except Exception as e:
                    print("Error while copying" + str(e))
                    continue 
                try:
                    with open("./assets/music/" + music_folder + "/config.json",'rt') as file_json:
                        old_config = json.load(file_json)
                        with open("./assets/music/" + music_folder + "/config.toml",'wt') as file_toml:
                            dump(old_config, file_toml)
                except Exception as e:
                    print("Error trying to convert the music format config file. Removing the folder")
                    try:
                        shutil.rmtree("./assets/music/" + music_folder)
                    except Exception as e2:
                        print("Error while trying to remove the folder. Music may be corrupted")
            else:
                print("Folder " + music_folder + " already existed on destination, omiting migration")

def get_all_music_available():
    ensure_assets_are_available()
    available_music = load_music_data()
    list = []
    for key in available_music.keys():
        list.append(key)
    list.append('rnd')
    return list

def is_music_available(music: str) -> bool:
    music = music.lower()
    available_music = get_all_music_available()
    available_music.append('rnd')
    return music in available_music
