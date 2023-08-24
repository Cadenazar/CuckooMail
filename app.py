from flask import Flask,request
app = Flask(__name__)
from datetime import date
today = date.today()
date_year = today.strftime("%Y")
date_mo = today.strftime("%m")
date_day = today.strftime("%d")
folder = date_year+"-"+date_mo+"-"+date_day


@app.route("/")
def hello():
    return "test"

@app.route("/submit",methods=['POST'])
def submit():
  try:
        # Check if the POST request has a file part
    if 'file' not in request.files:
      return "No file part", 400
  
    api_key = request.headers.get('api-key')
    file = request.files['file']
    if api_key != "api key you choose": #make sure to use the same api key for virus_checker.py
      print("Invalid API key was given, unauthorized access was attempted")
      return "Error authorized access", 401
        # If the user doesn't select a file, the browser will submit an empty part without filename
    if file.filename == '':
      print("no file name")
      return "No selected file", 400

        # Replace the following folder path with the actual path where you want to store the uploaded files
    file.save(file.filename)
    with open("malicious_files_central.json","w+") as mal_file:
      import json
      mal_file_dict = json.load(mal_file)
      with open(file.filename,"r") as new_mal_file:
        new_mal_file_dict = json.load(new_mal_file)
      for file in new_mal_file_dict:
        mal_file_dict[file] = new_mal_file_dict[file]
      json.dump(mal_file_dict, mal_file)      
    return "File submitted sucessfully",200
  except Exception as e:
    return(e)
if __name__ == "__main__":
    app.run(host='0.0.0.0')