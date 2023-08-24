# CuckooMail
Connect Postfix mail server to cuckoo sandbox vm, making postfix send all emails to a master email, where cuckoo sandbox vm will extract the emails from and analyse them. After that malicious files are automatically sent to a flask server hosted on the postfix mail server, which will run another program which deletes all malicious emails
