#!/usr/bin/python3

import os
import smtplib
import email.utils
import socket
from email.mime.text import MIMEText

notification_mail = "<YOUR_MAILADDR>"								# email address for notifications
ip_whitelist = ["127.0.0.1"]									# if the login ip is one of these, no notification will be sent out




ssh_ip =	os.environ['SSH_CONNECTION'].split(" ")[0]
ssh_user =	os.environ['USER']
hostname = 	socket.gethostname()
reverse_dns = ""

if ssh_ip not in ip_whitelist:
    try:
        reverse_dns = socket.gethostbyaddr(ssh_ip)[0]
    except:
        reverse_dns = "unknown"

    mail_msg =      "SSH login on " + str(hostname) + ":\n\nHost: " + str(hostname) + "\nfrom ip: " + str(ssh_ip) + " (" + str(reverse_dns) + ")\nssh user: " + str(ssh_user)
    sender_mail = "root@" + str(hostname)
    msg = MIMEText(mail_msg)
    msg['To'] = email.utils.formataddr((notification_mail, notification_mail))
    msg['From'] = email.utils.formataddr((hostname, sender_mail))
    msg['Subject'] = "ssh login for user " + str(ssh_user) + " on  " + str(hostname)
    server = smtplib.SMTP()
    server.connect ('localhost', 25)
    try:
        server.sendmail(notification_mail, [notification_mail], msg.as_string())
    finally:
        server.quit()

    
 

