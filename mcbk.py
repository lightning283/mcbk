import sys , os
from shutil import make_archive
from getpass import getuser
from pathlib import Path
import requests
import json
from anonfile import AnonFile
anon = AnonFile()
username = getuser()
if sys.platform == "linux":
    HOME = f"/home/{username}/.config/mcbk"
    MC_HOME = f"/home/{username}/.minecraft/"
    try:
        os.mkdir(HOME)
    except FileExistsError:
        pass
    if sys.argv[1] == "world" and sys.argv[2] == "backup":
        world_name = input("Enter World Name: ")
        if os.path.isdir(f"{HOME}/{world_name}"):
            pass
        else:
            os.system(f"cp -r '{MC_HOME}saves/{world_name}' {HOME}")
        os.chdir(f"{HOME}/")
        make_archive(world_name , "zip" , f"{HOME}/{world_name}")
        filename = f"{HOME}/{world_name}.zip"
        try:
            if sys.argv[3] == "upload":
                print("Uploading Files..")
                # https://github.com/awersli99/anonfile-upload
                url = 'https://api.anonfiles.com/upload'
                files = {'file': (open(filename, 'rb'))}
                r = requests.post(url, files=files)
                print("[UPLOADING]", filename)
                resp = json.loads(r.text)
                if resp['status']:
                    urlshort = resp['data']['file']['url']['short']
                    urllong = resp['data']['file']['url']['full']
                    print(f'[SUCCESS] Your file has been succesfully uploaded:\nFull URL: {urllong}\nShort URL: {urlshort}')
                else:
                    message = resp['error']['message']
                    errtype = resp['error']['type']
                    print(f'[ERROR] {message}\n{errtype}')
            else:
                pass
        except IndexError:
            pass
        desktop_dir = Path.home().joinpath('Desktop')
        os.system(f"cp -r '{filename}' {desktop_dir}")
        print("World Backup located at Desktop")
    else:
        pass
elif sys.platform == "windows":
    HOME = ""