# CuckooMail
Connect Postfix mail server to cuckoo sandbox vm, making Postfix send all emails to a master email, where cuckoo sandbox vm will extract the emails from and analyze them. After that malicious files are automatically sent to a Flask server hosted on the Postfix mail server, which will run another program that deletes all malicious emails

First, we need to configure the postfix server to send a copy of all emails to a master email user, so in this example, I would be creating a user called Cuckoo. Use the "adduser Cuckoo" command to create the new Cuckoo user, and enter the password and other details. Next, open the /etc/postfix/main.cf and add the line "always_bcc=Cuckoo@yourdomain.com". This will make Postfix always Blind carbon copy the Cuckoo users email, therefore the Cuckoo user will receive a copy of all mail sent through the postfix server. Now if u login into your Cuckoo users email, and send an email to any emails in your domain, you should receive a copy of the email inside the Cuckoos user inbox.

![image](https://github.com/Cadenazar/CuckooMail/assets/88576308/ec3a8a13-c3d4-4750-bb5e-70a9c863fa83)

Next, we need to configure your Cuckoo sandbox VM to constantly download all email attachments that is sent through the Postfix server. So first download the email_downloader.py script, and store it in a directory your cuckoo user can access. I recommend using the "/opt" directory, you can create a directory called cuckoo inside the "/opt" directory, creating a directory path that looks like "/opt/cuckoo". Remember to modify all the fields that need to be changed such as the host,username and password variables. This code made use of a large part of https://openthreat.ro/cuckoo-sandbox-email-attachment-reader-scanner the code from here. However it fixes some bugs and vulnerabilities in the code such as remote code execution through file name, the attacker sends 2 files with the same name but different content causing the script to download only the first file received and not allowing the running of files with spaces in their names. This was done by hashing the file content using SHA256 and using the file hash as the name of the downloaded file, therefore files with different file content but the same name will be named differently when downloaded.

We are going to make use of the cron service to run the email downloader script every 1 minute. So open the "/etc/crontab" file, and put in the line 
"*/1 * * * *     test    /usr/bin/python3.8 /opt/cuckoo/email_downloader.py >> email_downloader.log" this command will run the email_downloader script every minute and write all print outputs to the email_downloader.log file. You can now test the script by sending an email containing an attachment to any of your email addresses in your domain, after waiting for around a minute, Cuckoo sandbox should start running and analyzing the file. Remember to start your Cuckoo sandbox before testing the script.




