from smtpwned.providers import BaseProvider
import urllib.request
import json

class ResendProvider(BaseProvider):
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.resend.com/emails"
    
    def send_email(self, sender, to, subject, body, html=None):
        payload = {
            "from": sender,
            "to": [to] if isinstance(to, str) else to,
            "subject": subject,
            "text": body
        }
        if html:
            payload["html"] = html
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            request = urllib.request.Request(
                self.api_url,
                data=data,
                headers=headers,
                method="POST"
            )

            with urllib.request.urlopen(request, Timeout=10) as response:
                return response.status in (200,201)
        except Exception as error:
            print(f"Resend API Error: {error}")
            return False