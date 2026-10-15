import smtplib
from smtpwned.core.message import create_message

def connect_smtp(host,port):
    try:
        return smtplib.SMTP(host,port,timeout=10)
    except Exception as error:
        print(f'Connection failed: {error}')

server = connect_smtp('127.0.0.1',1025)

def send_message(server,msg):
    server.send_message(msg)

msg = create_message(
    'name <send@mail>',
    'receptient@mail',
    'theme',
    'body'
)

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




