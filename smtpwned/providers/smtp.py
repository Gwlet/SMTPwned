import smtplib
from smtpwned.core.message import create_message
from smtpwned.providers import BaseProvider

def connect_smtp(host, port):
    try:
        return smtplib.SMTP(host, port, timeout=10)
    except Exception as error:
        print(f'Connection failed: {error}')
        return None

def send_message(server, msg):
    return server.send_message(msg)

def enable_tls(server):
    server.ehlo()
    server.starttls()
    server.ehlo()

def login_smtp(server, username, password):
    server.login(username, password)

def connect_smtp_ssl(host, port):
    try:
        return smtplib.SMTP_SSL(host, port, timeout=10)
    except Exception as error:
        print(f"Error: {error}")
        return None

def connect(host, port, security="none"):
    if security == "ssl":
        server = connect_smtp_ssl(host, port)
        if server is None:
            raise RuntimeError(f'SSL Error: Failed to connect to {host}:{port}')
        return server
    
    elif security == "starttls":
        server = connect_smtp(host, port)
        if server is not None:
            try:
                enable_tls(server)
            except Exception as error:
                try:
                    server.close()
                except Exception:
                    pass
                raise error
        return server
    
    elif security == "none":
        server = connect_smtp(host, port)
        return server
    else:
        raise ValueError("Connect method not found, please try again")

def check_connection(server):
    if server is None or isinstance(server, bool):
        return False
    try:
        response = server.noop()[0]
        if response == 250:
            return True
        else:
            return False
    except Exception as error:
        print(f'Connection check failed: {error}')
        return False

def check_authentication(server, username, password):
    if server is None or isinstance(server, bool):
        return False
    try:
        login_smtp(server, username, password)
        print(f'Login successful for user: {username}')
        return True
    except Exception as error:
        print(f'Login failed: {error}')
        return False

def check_smtp_ready(server, username=None, password=None):
    if not check_connection(server):
        return False

    if username and password:
        return check_authentication(server, username, password)

    return True
def disconnect(server):
    try:
        server.quit()
        return True
    except Exception as error:
        print(f'Disconnection failed: {error}')
        return False

def close_connection(server):
    if server is not None and not isinstance(server, bool):
        return disconnect(server)
    else:
        print("Server is None, cannot close connection.")
        return False

def server_sendmail(server, sender, to, subject, body, html=None):
    if server is None or isinstance(server, bool):
        print("Error sending email: Invalid server connection")
        return False
    try:
        msg = create_message(sender, to, subject, body, html)
        result = send_message(server, msg)
        if result:
            print(f"Error sending email: {result}")
            return False
        print(f"Email sent successfully to {to}")
        return True
    except Exception as error:
        print(f"Error sending email: {error}")
        return False

def send_email_single_shot(host, port, username, password, sender, to, subject, body, html=None, security="starttls"):
    connection = None
    try:
        connection = connect(host, port, security)

        if connection is None:
            print("Error: Failed to establish connection.")
            return False

        check_ready = check_smtp_ready(connection, username, password)

        if not check_ready:
            return False
        
        return server_sendmail(connection, sender, to, subject, body, html)

    finally:
        if connection is not None:
            close_connection(connection)

# class SMTPProvider(BaseProvider):
#     def __init__(self, host, port, username, password, security="starttls"):
#         self.host = host
#         self.port = port
#         self.username = username
#         self.password = password
#         self.security = security

#     def send_email(self, sender, to, subject, body, html=None, security="none"):
#         sec = security or getattr(self, 'security', 'none')

#         return send_email_single_shot(
#             self.host,
#             self.port,
#             self.username,
#             self.password,
#             sender,
#             to, 
#             subject,
#             body,
#             html,
#             security)

class SMTPProvider(BaseProvider):

    def __init__(self, host, port, username, password, security="starttls"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.security = security

    def send_email(
        self, sender, to, subject, body, html=None, security=None
    ):
        sec = security or getattr(self, "security", "none")

        return send_email_single_shot(
            self.host,
            self.port,
            self.username,
            self.password,
            sender,
            to,
            subject,
            body,
            html,
            sec,
        )