from pathlib import Path
import requests
import json
from datetime import date
today = date.today()
date_year = today.strftime("%Y")
date_mo = today.strftime("%m")
date_day = today.strftime("%d")
folder = date_year+"-"+date_mo+"-"+date_day
wait_list = []
def cuckoo_sandbox_checker(analysis_id):
   with open(f".cuckoo/storage/analyses/{analysis_id}/reports/report.json","r") as report:
     report_json = json.load(report)
     #do whatever checks you want here
   result = True #change your malware detection criteria here
   return(result)
      
def update_mal_file(folder,file,file_json):
  try:
    with open(f"/home/user/malicious_files_{folder}.json","r") as mal_files:  #change this file directory to your home directory, can be any directory but make sure to change the rest of the code
      mal_file_json = json.load(mal_files)
      mal_file_json[file] = file_json[file]["content"]
  except:
      mal_file_json = {}
      mal_file_json[file] = file_json[file]["content"]
  with open(f"/home/user/malicious_files_{folder}.json","w") as mal_files:  #change this file directory to your home directory, can be any directory but make sure to change the rest of the code
      json.dump(mal_file_json,mal_files)

with open(f"/home/user/filename_to_content_{folder}.json","r") as files: #change this file directory to your home directory, can be any directory but make sure to change the rest of the code
   file_json = json.load(files)
headers = {
    "accept": "application/json",
    "x-apikey": "Virus total api key" #use your virus total api key here
}
for file in file_json:
  if file_json[file]["checked"] == False:
    file_hash = Path(file).stem
    cuckoo_sandbox_check = cuckoo_sandbox_checker(file_json["file"]["id"]) #Uses the analysis ID of the file to get the report.json from cuckoo sandbox
    if cuckoo_sandbox_check == False: #Malicious file detected
       update_mal_file(folder,file,file_json)
       break
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    try:
      response = requests.get(url, headers=headers)
      response_json = json.loads(response.text)
      anti_virus_check  = response_json["data"]["attributes"]["last_analysis_results"]   
      sandbox_check = {}
      try:
        if anti_virus_check == {}:
          sandbox_check = response_json["data"]["attributes"]["sandbox_verdicts"]["Zenbox"]["category"]
          confidence_lvl = response_json["data"]["attributes"]["sandbox_verdicts"]["Zenbox"]["confidence"]
      except:
        raise Exception("Virus total has not analysed file yet")
      print("json",response_json)
      for anti_virus in anti_virus_check:
          if anti_virus_check[anti_virus]["category"] == "malicious" or (sandbox_check == "malicious" and confidence_lvl > 30):
            update_mal_file(folder,file,file_json)
            url = "https://domain.com:5000/submit" #change this to your mail-server/ flask server domain
            form_data = {'file': open(f"/home/user/malicious_files_{folder}.json","r")}  #change this file directory to your home directory, can be any directory but make sure to change the rest of the code
            auth_headers =  {'api-key':'flask api key'} # change to the one you use later on in the project
            server = requests.post(url, files=form_data,headers=auth_headers)
            print("\n\n",server.text)
            if "File submitted sucessfully" not in server.text:
              url = "https://backup-domain.com:5000/submit" #change this to your mail-server/ flask server domain
              form_data = {'file': open(f"/home/user/malicious_files_{folder}.json","r")} #change this file directory to your home directory, can be any directory but make sure to change the rest of the code
              server = requests.post(url, files=form_data)

            break
    except Exception as e:
      wait_list.append(file)
with open(f"/home/user/filename_to_content_{folder}.json","w") as files:  #change this file directory to your home directory, can be any directory but make sure to change the rest of the code
   for file in file_json:
     if file not in wait_list:
       file_json[file]["checked"] = True
   file_json = json.dump(file_json,files)
