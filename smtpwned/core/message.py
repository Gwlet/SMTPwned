from email.message import EmailMessage

def create_message (sender, to, subject, body, html=None):
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)
    if html is not None:
        msg.add_alternative(html, subtype='html')
    
    return msg

msg = create_message(
    'send@mail',
    'receptient@mail',
    'theme',
    'Test body content',
    '<button>Test button</button>'
)


print(msg)