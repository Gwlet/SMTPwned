import json
import urllib.error
import urllib.request

from smtpwned.providers import BaseProvider


class ResendProvider(BaseProvider):

    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.resend.com/emails"

    def send_email(self, sender, to, subject, body, html=None):
        payload = {
            "from": sender,
            "to": [to] if isinstance(to, str) else to,
            "subject": subject,
            "text": body,
        }
        if html:
            payload["html"] = html

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "SMTPwned/1.0",  # Обход Cloudflare 1010
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            request = urllib.request.Request(
                self.api_url, data=data, headers=headers, method="POST"
            )

            with urllib.request.urlopen(request, timeout=10) as response:
                if response.status in (200, 201):
                    return True, "Email sent successfully!"
                else:
                    return False, f"Server returned status {response.status}"

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            return False, f"HTTP {e.code}: {error_body}"

        except Exception as error:
            return False, f"API Error: {error}"