# SMTPwned

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12+" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License" />
  <img src="https://img.shields.io/badge/Status-Active-4CAF50?style=for-the-badge" alt="Active" />
</p>

Open-source SMTP security and email testing toolkit for validating delivery, authentication flows, and infrastructure-level email configurations.

SMTPwned helps security researchers, developers, and mail administrators test SMTP behavior, inspect DNS and mail policy records, and send messages through both direct SMTP and Resend API integrations.

## Why SMTPwned?

Email systems are notoriously difficult to debug. Small configuration mistakes can break delivery, trigger spam filtering, or expose authentication issues. SMTPwned provides a focused toolkit to:

- send mail over SMTP with configurable security modes
- test Resend-based delivery flows
- validate DNS/MX records
- inspect SPF and DMARC posture
- prototype email-related security checks in a single interface

## Features

- SMTP sender with optional TLS/SSL support
- Resend API message delivery integration
- DNS/MX lookup tooling
- SPF and DMARC checking workflow
- Lightweight terminal-style interface built with Textual
- Python-first project structure for easy extension

## Installation

### From source

```bash
git clone https://github.com/Gwlet/SMTPwned.git
cd SMTPwned
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .
```

### Run the app

```bash
smtpwned
```

Or:

```bash
python -m smtpwned
```

## Quick Start

### SMTP sending example

```python
from smtpwned.providers.smtp import SMTPProvider

provider = SMTPProvider(
    host="smtp.gmail.com",
    port=587,
    username="you@gmail.com",
    password="your-app-password",
    security="starttls",
)

success = provider.send_email(
    sender="you@gmail.com",
    to="recipient@example.com",
    subject="SMTPwned test",
    body="Hello from SMTPwned!",
)

print("sent" if success else "failed")
```

### Resend API example

```python
from smtpwned.providers.resend import ResendProvider

provider = ResendProvider(api_key="re_xxx")

success, message = provider.send_email(
    sender="noreply@example.com",
    to="recipient@example.com",
    subject="Resend test",
    body="Hello from SMTPwned via Resend.",
)

print(success, message)
```

## Project Structure

```text
SMTPwned/
├── smtpwned/
│   ├── __init__.py
│   ├── __main__.py
│   ├── app.py
│   ├── app.tcss
│   ├── core/
│   │   └── message.py
│   ├── diagnostics/
│   │   └── dns.py
│   └── providers/
│       ├── __init__.py
│       ├── smtp.py
│       └── resend.py
├── templates/
├── tests/
│   └── test_message.py
├── LICENSE
├── README.md
├── pyproject.toml
└── .gitignore
```

## Core components

### SMTP provider

The SMTP provider layer handles connection setup, authentication, TLS negotiation, and message sending. It supports:

- plain SMTP
- STARTTLS
- SSL/TLS wrapping

### Resend provider

The Resend provider supports sending mail through the Resend API, which is useful for testing delivery workflows and verifying infrastructure assumptions.

### Mail message builder

`smtpwned.core.message.create_message()` constructs an email payload using Python's standard library `EmailMessage` type, making it easy to build both plain-text and HTML messages.

## Roadmap

This project is designed for practical testing and experimentation. Planned areas of focus include:

- stronger DNS validation utilities
- expanded SPF/DKIM/DMARC checks
- policy-driven email diagnostics
- richer output and reporting for scan results
- improved reliability and validation of provider flows

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add or update tests where relevant
5. Open a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Community and Contact

- Repository: https://github.com/Gwlet/SMTPwned
- Author: @Gwlet

## Acknowledgements

Built for email security testing, mail infrastructure validation, and practical SMTP experimentation.

---

Made with Python and a focus on practical email diagnostics.
