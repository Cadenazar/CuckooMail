# CuckooMail
Connect Postfix mail server to cuckoo sandbox vm, making Postfix send all emails to a master email, where cuckoo sandbox vm will extract the emails from and analyze them. After that malicious files are automatically sent to a Flask server hosted on the Postfix mail server, which will run another program that deletes all malicious emails

First, we need to configure the postfix server to send a copy of all emails to a master email user, so in this example, I would be creating a user called Cuckoo. Use the "adduser Cuckoo" command to create the new Cuckoo user, and enter the password and other details. Next, open the /etc/postfix/main.cf and add the line "always_bcc=Cuckoo@yourdomain.com". This will make Postfix always Blind carbon copy the Cuckoo users email, therefore the Cuckoo user will receive a copy of all mail sent through the postfix server. Now if u login into your Cuckoo users email, and send an email to any emails in your domain, you should receive a copy of the email inside the Cuckoos user inbox.
![image](https://github.com/Cadenazar/CuckooMail/assets/88576308/ec3a8a13-c3d4-4750-bb5e-70a9c863fa83)

Next, we need to configure your Cuckoo sandbox VM to constantly download all email attachments that is sent through the Postfix server. So first download the email_downloader.py script, and store it in a directory your cuckoo user can access. I recommend using the "/opt" directory, you can create a directory called cuckoo inside the "/opt" directory, creating a directory path that looks like "/opt/cuckoo". Remember to modify all the fields that need to be changed such as the host,username and password variables. This code made use of a large part of https://openthreat.ro/cuckoo-sandbox-email-attachment-reader-scanner the code from here. However it fixes some bugs and vulnerabilities in the code such as remote code execution through file name, the attacker sends 2 files with the same name but different content causing the script to download only the first file received and lastly the orginal code does not allow the running of files with spaces in their names. This was done by hashing the file content using SHA256 and using the file hash as the name of the downloaded file, therefore files with different file content but the same name will be named differently when downloaded.

We are going to make use of the cron service to run the email downloader script every 1 minute. So open the "/etc/crontab" file, and put in the line 
"*/1 * * * *     user    /usr/bin/python3.8 /opt/cuckoo/email_downloader.py >> email_downloader.log" this command will run the email_downloader script every minute and write all print outputs to the email_downloader.log file.You might need to change your python version, path, and user. You can now test the script by sending an email containing an attachment to any of your email addresses in your domain, after waiting for around a minute, Cuckoo sandbox should start running and analyzing the file. Remember to start your Cuckoo sandbox before testing the script. Also, remember to enable send file to virustotal to analyse inside the cuckoo sandbox config. You can do this by opening the ".Cuckoo/conf/processing.conf" file. Enable VirusTotal by setting the enabled field to yes and Scan field to yes. This will send all analyzed files to virustotal for further analysis.

![image](https://github.com/Cadenazar/CuckooMail/assets/88576308/21af695c-0283-41ec-8694-6377130d41e3)


Next we are going to make use of the cron service to retrieve the results of the analysis from Virustotal, I have not gotten the time to write the code for CuckooSandbox analysis results. However a general idea of how it can be done is, open the folder corresponding to the file u analyzed stored inside the ".cuckoo/storage/analyses" folder, for example in the example below, analysis number 1 is the only file I analyzed.

![image](https://github.com/Cadenazar/CuckooMail/assets/88576308/48232c8e-11ed-4620-8fe9-65ae0b199784)

Open the reports folder and inside there is a "report.json" file stored inside. By parsing the file and reading the contents, you can look for certain elements that are suspicious and relevant to malware files. For example, your Word documents and powerpoints make calls to an unknown IP address, or maybe certain virus signatures are found.

![image](https://github.com/Cadenazar/CuckooMail/assets/88576308/3ceef878-919c-49eb-b534-eaaf8a8c0bb7)


However, with the current virus_checker.py code, you are able to make use of virus total to delete malicious files. So firstly we need to download the file. Next, remember to modify all paths to fit the directory where the email_downloader.py stores all its jsons, the default should be your home directory. Remeber to change the VirusTotal api key to a valid one. I would be using the "/opt/virus_checker" directory to store the file. Next, open the "/etc/crontab" file and add the line 
"*/1 * * * *     test    /usr/bin/python3.8 /opt/virus_checker/virus_checker.py  >> virus_checker.log"
This would make the cron service run the virus_checker.py code every minute. You might need to change your python version, path, and user. Now you can test the code by sending an email to any emails in your domain, once Cuckoo sandbox and virus_total has finished analyzing the results, in a short moment you can look inside the virus_checker.log file, to see if the virus_total results were returned. The flask server you are sending to will give an error however that will be fixed later.

![image](https://github.com/Cadenazar/CuckooMail/assets/88576308/48c345dd-1cf4-4ff9-9a4a-82334922d409)




