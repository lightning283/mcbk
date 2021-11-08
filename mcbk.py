import sys,os,json,shutil
from getpass import getuser
from pathlib import Path
from shutil import make_archive

import requests


def main():
    zipped_file = None
    mc_path = get_path()
    if sys.argv[1] == "backup":
        backup(mc_path)

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
    arg = sys.argv[2]                  
    if arg == "world":
        if sys.platform == "linux":
            mc_path = mc_path + '/saves'
        else:
            mc_path = Path.home().joinpath('AppData').joinpath('Roaming').joinpath('.minecraft').joinpath('saves')
        target = input("Enter World Name: ")
    elif arg == "mods":
        target = "mods"
    elif arg == "shaderpacks":
        target = "shaderpacks"
    elif arg == "all":
        target = ".minecraft"
        mc_path = Path().home()
    desktop_dir = Path.home().joinpath('Desktop')
    os.chdir(mc_path)
    print("Compressing please wait..")
    make_archive(target , 'zip' , f"{mc_path}/{target}")
    # os.system(f"cp -r '{target}.zip' {desktop_dir}")
    shutil.copy(f'{target}.zip', desktop_dir)
    os.remove(f"{target}.zip")
    if os.path.isfile(f"{desktop_dir}/.minecraft.zip"):
        os.rename(f"{desktop_dir}/.minecraft.zip", f"{desktop_dir}/minecraft.zip")
        target = "minecraft"
    print("Backup located at Desktop : " + target)
    os.chdir(desktop_dir)
    open_location()
    try:
        if "upload" in sys.argv:
            anon_upload(f"{target}.zip")
    except IndexError:
        pass


if __name__ == "__main__":
    main()
