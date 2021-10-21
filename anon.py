#!/usr/bin/env python3

import requests
import json

url = 'https://api.anonfiles.com/upload'
filename = "README.md"
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
