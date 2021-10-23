import sys , os
from shutil import make_archive , copyfile
from getpass import getuser
from pathlib import Path
import requests
import json
desktop_dir = Path.home().joinpath('Desktop')
username = getuser()
def anon_upload(filename):
    print("[UPLOADING]", filename)
    # https://github.com/awersli99/anonfile-upload
    url = 'https://api.anonfiles.com/upload'
    files = {'file': (open(filename, 'rb'))}
    r = requests.post(url, files=files)
    resp = json.loads(r.text)
    if resp['status']:
        urlshort = resp['data']['file']['url']['short']
        urllong = resp['data']['file']['url']['full']
        print(f'[SUCCESS] Your file has been succesfully uploaded:\nFull URL: {urllong}\nShort URL: {urlshort}')
    else:
        message = resp['error']['message']
        errtype = resp['error']['type']
        print(f'[ERROR] {message}\n{errtype}')
if sys.platform == "linux":
    MC_HOME = f"/home/{username}/.minecraft/saves"
    if sys.argv[1] == "backup":
        if sys.argv[2] == "world":
            world_name = input("Enter World Name: ")
            os.chdir(MC_HOME)
            make_archive(world_name , "zip" , f"{MC_HOME}/{world_name}")
            filename = f"{MC_HOME}/{world_name}.zip"
            try:
                if sys.argv[3] == "upload":
                    anon_upload(filename)
                else:
                    pass
            except IndexError:
                pass
            os.system(f"cp -r '{filename}' {desktop_dir}")
            print("World Backup located at Desktop")
        elif sys.argv[2] == "mods":
            pass
        elif sys.argv[2] == "shaders":
            pass
        elif sys.argv[2] == "all":
            pass
        else:
            print("")
            print("Error Invalid Argument")
            print("Possible Options are:")
            print(" mcbk backup world")
            print(" mcbk backup mods")
            print(" mcbk backup shaders")
            print(" mcbk backup all")
            print("If You want the backed up file to be uploaded  , use 'upload' as the final argument.")
    else:
        pass
elif sys.platform == "win32":
    HOME = Path.home()
    MC_HOME = Path.home().joinpath('AppData').joinpath('Roaming').joinpath('.minecraft').joinpath('saves')
    os.chdir(HOME)
    if sys.argv[1] == "backup":
        if sys.argv[2] == "world":
            world_name = input("Enter World Name: ")
            os.chdir(MC_HOME)
            make_archive(world_name , 'zip' , f"{MC_HOME}/{world_name}")
            try:
                if sys.argv[3] == "upload":
                    anon_upload(f"{world_name}.zip")
                else:
                    pass
            except IndexError:
                pass
            os.system("start explorer .")
            
        elif sys.argv[2] == "mods":
            pass
        elif sys.argv[2] == "shaders":
            pass
        elif sys.argv[2] == "all":
            pass
        else:
            print("")
            print("Error Invalid Argument")
            print("Possible Options are:")
            print(" mcbk backup world")
            print(" mcbk backup mods")
            print(" mcbk backup shaders")
            print(" mcbk backup all")
            print("If You want the backed up file to be uploaded  , use 'upload' as the final argument.")
    else:
        pass