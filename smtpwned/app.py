from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Select, Button, Header, Footer, Static, Input, TabbedContent, TabPane, Label
from smtpwned.providers.smtp import SMTPProvider
from textual.containers import Horizontal, Grid
import time
from smtpwned.providers.resend import ResendProvider

class SMTPwnedApp(App):
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static('SMTPwned (Beta 1.0)', id='title_text')

        with TabbedContent(id='tabbed_content'):

            with TabPane('SMTP Sender', id='smtp_tab'):

                yield Input(placeholder='Enter SMTP server address(e.g. smtp.gmail.com):', id='smtp_host')
                yield Input(placeholder='Enter port(e.g. 587):', id='smtp_port')
                yield Input(placeholder='Username/Email:', id='smtp_email')
                yield Input(placeholder='Password:', password=True, id='smtp_password')

                yield Input(placeholder='Recipient(To) Email:', id='smtp_recipe')
                yield Input(placeholder='Subject:', id='smtp_subject')
                yield Input(placeholder='Enter body message:', id='smtp_body')
                
                yield Select(
                    options=[
                        ("None", "none"),
                        ("SSL", "ssl"),
                        ("STARTTLS", "starttls")
                    ], 
                    value="none",
                    allow_blank=False,
                    prompt="Select Security Type",
                    id="security_select"
                )

                with Grid(id='smtp_button_container'):
                    yield Button("Send Email", variant='success', id='smtp_btn')

                    
                yield Static('Status: Disconnected', id='smtp_status')

            with TabPane('Resend Sender', id='Resend_tab'):
                    
                    yield Input(placeholder='Enter Resend API key', id='resend_api')
                    yield Input(placeholder='Enter Sender Mail and Name(e.g. example <example@domen.com>)', id='resend_mail')
                    yield Input(placeholder='Enter Recipient Mail', id='resend_recipe')
                    yield Input(placeholder='Subject:', id='resend_subject')
                    yield Input(placeholder='Enter body message:', id='resend_body')

                    with Grid(id='resend_button_container'):
                        yield Button("Send Email", variant='success', id='resend_btn')
                        
                    yield Static('Status: Disconnected', id='resend_status')

            with TabPane("Exit", id="exit_tab"):
                pass
                
        
        yield Footer()
            

    @on(Button.Pressed, '#smtp_btn')
    def on_send_click(self, event:Button.Pressed) -> None:
        self.send_email()

    @on(Button.Pressed, '#resend_btn')
    def on_resend_click(self, event:Button.Pressed) -> None:
        self.resend_email()

    @on(TabbedContent.TabActivated)
    def tab_exit_active(self, event:TabbedContent.TabActivated) -> None:
        if event.pane.id == "exit_tab":
            self.exit()

    @work(thread=True)
    def send_email(self) -> None:
        active_tab = self.query_one('#tabbed_content', TabbedContent).active
        if active_tab == "smtp_tab":
            status = self.query_one('#smtp_status', Static)
            status.update('Status: Sending email...')

            host = self.query_one('#smtp_host', Input).value
            port = self.query_one('#smtp_port', Input).value
            username = self.query_one('#smtp_email', Input).value
            password = self.query_one('#smtp_password', Input).value
            to = self.query_one('#smtp_recipe', Input).value
            subject = self.query_one('#smtp_subject', Input).value
            body = self.query_one('#smtp_body', Input).value
            security = self.query_one('#security_select', Select).value


            
            try:
                port = int(port)
            except ValueError:
                self.query_one('#smtp_status', Static).update('Status: Invalid port number')
                return

            auth_user = username if username.strip() else None
            auth_pass = password if password.strip() else None

            sender_address = username.strip() if username.strip() else "test@localhost"

            provider = SMTPProvider(
                host=host,
                port=port,
                username=auth_user,
                password=auth_pass,
                security=security
            )

            try:
                success = provider.send_email(
                    sender=sender_address,
                    to=to,
                    subject=subject,
                    body=body,
                    security=security
                )
                if success:
                    self.query_one('#smtp_status', Static).update('Status: Email sent successfully!')
                else:
                    self.query_one('#smtp_status', Static).update('Status: Failed (Returned False from provider)')
            except Exception as err:
                self.query_one('#smtp_status', Static).update(f'Error: {type(err).__name__}: {err}')


    @work(thread=True)
    def resend_email(self) -> None:
        status = self.query_one('#resend_status', Static)
        status.update('Status: Sending email...')

        api_key = self.query_one('#resend_api', Input).value
        sender = self.query_one('#resend_mail', Input).value
        to = self.query_one('#resend_recipe', Input).value
        subject = self.query_one('#resend_subject', Input).value
        body = self.query_one('#resend_body', Input).value

        provider = ResendProvider(api_key=api_key)

        try:
            success, msg = provider.send_email(
            sender=sender, to=to, subject=subject, body=body
        )

            if success:
                status.update("Status: Email sent successfully!")
            else:
                status.update(f"Failed: {msg}")
        
        except Exception as err:
            self.query_one('#resend_status', Static).update(f'Error: {type(err).__name__}: {err}')
if __name__ == "__main__":
    app = SMTPwnedApp()
    app.run()
