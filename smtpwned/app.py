from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static, Input
from smtpwned.providers.smtp import SMTPProvider

class SMTPwnedApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static('SMTPwned (Beta 0.1)')

        yield Input(placeholder='Enter SMTP server address(e.g. smtp.gmail.com):', id='host_input')
        yield Input(placeholder='Enter port(e.g. 587):', id='port_input')
        yield Input(placeholder='Username/Email:', id='email_input')
        yield Input(placeholder='Password:', password=True, id='password_input')

        yield Input(placeholder='Recipient(To) Email:', id='recipient_input')
        yield Input(placeholder='Subject:', id='subject_input')

        yield Button("Send Email", variant='success', id='send_btn')

        yield Static('Status: Disconnected', id='status_text')
        yield Footer()

    @on(Button.Pressed, '#send_btn')
    def on_send_click(self, event:Button.Pressed) -> None:
        self.send_email_worker()

        @work(thread=True)
        def send_email(self) -> None:
            status = self.query_one('#status_text', Static)
            status.update('Status: Sending email...')

            host = self.query_one('#host_input', Input).value
            port = self.query_one('#port_input', Input).value
            username = self.query_one('#email_input', Input).value
            password = self.query_one('#password_input', Input).value
            to = self.query_one('#recipient_input', Input).value
            subject = self.query_one('#subject_input', Input).value

            try:
                port = int(port)
            except ValueError:
                self.query_one('#status_text', Static).update('Status: Invalid port number')
                return

            provider = SMTPProvider(host=host, port=port, username=username, password=password)
            success = provider.send_email(
                sender=username,
                to=to,
                subject=subject,
                body="This is a test email sent from SMTPwned."
            )
            if success:
                self.query_one('#status_text', Static).update('Status: Email sent successfully!')
            else:
                self.query_one('#status_text', Static).update('Status: Failed to send email.')

if __name__ == "__main__":
    app = SMTPwnedApp()
    app.run()