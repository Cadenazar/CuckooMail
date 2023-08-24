import os
import pwd
import json
from datetime import date
today = date.today()
date_year = today.strftime("%Y")
date_mo = today.strftime("%m")
date_day = today.strftime("%d")
folder = date_year+"-"+date_mo+"-"+date_day

try:
  with open(f"/home/user/flask_directory/malicious_{folder}.json","rb") as file: #change to directory you are using for app.py, flask directory
    mal_file_dict = json.load(file)
except FileNotFoundError:
    pass
except Exception as e:
    print(e)

user_lst = pwd.getpwall()
mail_user_lst = []
#look for all mail users inside list of local and system users
for user in user_lst:
  if "/home" in user[5] and user[0] != "syslog" and user[0] != "ubuntu":
    mail_user_lst.append(user[0])
# delete email if file attachment matches a malicious file name
# found in cuckoo sandbox
for mail_user in mail_user_lst:
  try:
    mail_dir = "/home/"+mail_user+"/Maildir/cur"
    for file in os.listdir(mail_dir):
      with open(mail_dir+"/"+file,"rb") as emails:
        email = emails.read()
        for mal_file in mal_file_dict:
            mal_file_content = mal_file_dict[mal_file]
            if mal_file_content.encode() in email.replace(b"\n",b""):
              os.remove(mail_dir+"/"+file)
  except:
    pass
