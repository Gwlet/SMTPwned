import smtplib
from smtpwned.core.message import create_message

def connect_smtp(host,port):
    try:
        return smtplib.SMTP(host,port,timeout=10)
    except Exception as error:
        print(f'Connection failed: {error}')

def send_message(server,msg):
    server.send_message(msg)

def enable_tls(server):
    server.ehlo()
    server.starttls()
    server.ehlo()

def login_smtp(server,username,password):
    server.login(username,password)

def connect_smtp_ssl(host,port):
    try:
        return smtplib.SMTP_SSL(host,port,timeout=10)
    except Exception as error:
        print(f"Error: {error}")


#ONLY FOR TEST

'''
server = connect_smtp('127.0.0.1',1025)

if server is not None:
    print('Connected')
    try:
        send_message(server,msg)
        print('Message sent')
    except Exception as error:
        print(f'Error: {error}')
    finally:
        server.quit()
    
else:
    print('Not connected')
'''



