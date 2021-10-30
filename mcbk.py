import json
import os
import sys
from getpass import getuser
from pathlib import Path
from shutil import make_archive

import requests


def main():
    zipped_file = None
    mc_path = get_path()

    os.chdir(f"{mc_path}/saves")

    if sys.argv[1] == "backup":
        backup(f"{mc_path}/saves")
    try:
        if "upload" in sys.argv:
            os.chdir(f"{mc_path}/saves")
            anon_upload(f"{backup.world_name}.zip")
    except IndexError:
        pass

# returns minecraft path ( differs between operating system )
def get_path():
    mc_home = None

    if sys.platform == "linux":
        mc_home = f"/home/{getuser()}/.minecraft"
    elif sys.platform == "win32":
        mc_home = Path.home().joinpath('AppData').joinpath('Roaming').joinpath('.minecraft')

    return mc_home


# uploads the file in cloud ( anon files )
def anon_upload(filename):
    print("[UPLOADING]", filename)
    # https://github.com/awersli99/anonfile-upload
    url = 'https://api.anonfiles.com/upload'
    files = {'file': (open(filename, 'rb'))}
    post_request = requests.post(url, files=files)
    resp = json.loads(post_request.text)

    if resp['status']:
        url_short = resp['data']['file']['url']['short']
        url_long = resp['data']['file']['url']['full']
        print(f'[SUCCESS] Your file has been successfully uploaded:\nFull URL: {url_long}\nShort URL: {url_short}')
    else:
        message = resp['error']['message']
        error_type = resp['error']['type']
        print(f'[ERROR] {message}\n{error_type}')
def open_location():
    if sys.platform == "win32":
        os.system("explorer .")
    elif sys.platform == "linux":
        os.system("dolphin .")

# makes backup zip of  : world , mods , shaders , etc
def backup(mc_path):
    desktop_dir = Path.home().joinpath('Desktop')

    arg = sys.argv[2]

    target = None

    if arg == "world":
        backup.world_name = input("Enter World Name: ")
        world_name = backup.world_name
        target = world_name
        make_archive(world_name, "zip", f"{mc_path}/{target}")
        zipped_file = f"{mc_path}/{target}.zip"
        os.system(f"cp -r '{zipped_file}' {desktop_dir}")
        os.remove(zipped_file)
        print("Backup located at Desktop : " + target)
        os.chdir(desktop_dir)
        open_location()
    elif arg == "mods":
        pass
    elif arg == "shaderpacks":
        pass

if __name__ == "__main__":
    main()
