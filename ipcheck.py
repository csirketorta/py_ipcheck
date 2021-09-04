import urllib.request
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from godaddypy import Client, Account
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

my_godaddy = Account(api_key='PUBLIC', api_secret='SECRET')

os.chdir('/path/to/dir')

sender_address = 'sm1@gmail.com'
sender_pass = 'SSPw123'
recipient = 'rec1@domain.com'
recipient2 = 'rec2@domain.com'
message = MIMEMultipart()

message['From'] = sender_address
message['To'] = recipient
message['Subject'] = 'IP address changed'

req = Request("https://ident.me")
try:
    response = urlopen(req)
except HTTPError as e:
    print('The server couldn\'t fulfill the request.')
    print('Error code: ', e.code)
    exit()
except URLError as e:
    print('We failed to reach a server.')
    print('Reason: ', e.reason)
    exit()
else:
    print('ident.me up and running')
    new_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    try:
        f = open("ip_old.txt", "r")
        old_ip = f.read()
    except OSError:
        with open("ip_old.txt", "w+") as file_object:
            file_object.write("127.0.0.1")
            file_object.close()
            f = open("ip_old.txt", "r")
            old_ip = f.read()

    if new_ip != old_ip:
        print("Regi: " + old_ip)
        print("Uj: " + new_ip)
        with open("ip_old.txt", "w+") as file_object:
            file_object.write(new_ip)
        mail_content = '''IP address changed. \r\nOld IP address: ''' + old_ip + ''' \r\nNew IP address: ''' + new_ip

        client = Client(my_godaddy)
        client.get_records('mydomain.tld')
        client.update_ip(new_ip, domains=['mydomain.tld'])
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, recipient, text)
        session.sendmail(sender_address, recipient2, text)
        session.quit()
        
