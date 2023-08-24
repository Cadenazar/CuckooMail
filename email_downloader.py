import base64
import os
from imbox import Imbox
import traceback
import datetime
from datetime import date
import pathlib
import time
import hashlib
import pathlib

#mail server host + credentials variables
host = "mail server host eg. smtp.gmail.com (gmail mail server)"
username = "username for master mail user eg. the mail cuckoo sandbox sends everything to"
password = "password for master mail user"

#no need to change this variables
today = date.today()
date_year = today.strftime("%Y")
date_mo = today.strftime("%m")
date_day = today.strftime("%d")
folder = date_year+"-"+date_mo+"-"+date_day
download_folder = "."
path = os.path.join(download_folder, folder)

# Create daily folder
if not os.path.exists(path):
  os.mkdir(path)

if not os.path.isdir(download_folder):
    os.makedirs(download_folder, exist_ok=True)

# Connect to mail server
mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=None, starttls=False)
messages = mail.messages(date__on=datetime.date(int(date_year), int(date_mo), int(date_day)))
# Iterate mails, download attachments, submit to sandbox
for (uid, message) in messages:
    mail.mark_seen(uid)

    for idx, attachment in enumerate(message.attachments):
        try:
            att_fn = attachment.get('filename')
            print(att_fn)
            file_content = attachment.get("content").read()
            sha256 = hashlib.sha256()
            sha256.update(file_content)
            file_hash = sha256.hexdigest()
            file_extension = pathlib.Path(att_fn).suffix
            download_path = f"{path}/{file_hash}{file_extension}"
            if not os.path.exists(download_path):
                with open(download_path, "wb") as fp:
                    fp.write(file_content)
                    cmd = "/usr/local/bin/cuckoo submit" + " " + download_path #change to cuckoo file path
                    #print(cmd)
                    os.system(cmd)
                    file_content_string = (base64.b64encode(file_content)).decode("ascii")
                    import json
                    stored_json = {}
                    try:
                      with open(f'filename_to_content_{folder}.json', 'r') as outfile:
                        stored_json = json.load(outfile)
                    except:
                      pass
                    finally:
                     stored_json[file_hash+file_extension] = {"content":file_content_string,"checked":False}
                     with open(f'filename_to_content_{folder}.json','w') as outfile:
                        json.dump(stored_json,outfile)
        except:
            pass
            print(traceback.print_exc())

#log out from mail server
mail.logout()