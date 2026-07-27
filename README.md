# 📬 Project Inbox

A lightweight, modular command-line email client built in Python that supports sending and receiving emails using the IMAP and SMTP protocols.

Project Inbox provides a simple terminal interface for authenticating with email providers, browsing mailboxes, reading messages, downloading attachments, and composing emails without leaving the command line.

---

## Features

* Secure IMAP and SMTP authentication
* Gmail support
* Support for custom IMAP/SMTP servers
* View inbox with paginated email listing
* Read plain text and HTML emails
* MIME-compliant email parsing
* RFC 2047 encoded header decoding
* Download email attachments
* Compose and send emails with multiple attachments
* Cross-platform terminal interface (Windows, Linux, macOS)
* Modular architecture separating authentication, mailbox navigation, email parsing, and email composition

---

## Project Structure

```text
Project-Inbox/
│
├── main.py          # Application entry point
├── viewmail.py      # Inbox navigation and pagination
├── parse.py         # Email parsing and attachment handling
├── sendmail.py      # Email composition and SMTP sending
├── requirements.txt
└── README.md
```

---

## Technologies Used

* Python 3
* IMAP (`imaplib`)
* SMTP (`smtplib`)
* Python Email Package (`email`)
* BeautifulSoup4

---

## Installation

Clone the repository:

```bash
git clone https://github.com/pseudowudo/Project-Inbox.git
cd Project-Inbox
```

Install the required dependency:

```bash
pip install -r requirements.txt
```

---

## Gmail Authentication

> **Important**
>
> Google no longer allows authentication with your normal Gmail password for IMAP/SMTP access.
>
> To use Project Inbox with Gmail, you **must generate a Google App Password** and use it instead of your account password when logging in.
>
> Steps:
>
> 1. Enable **2-Step Verification** on your Google account.
> 2. Go to **Google Account → Security → App Passwords**.
> 3. Generate a new App Password for **Mail**.
> 4. Use the generated 16-character password when logging into Project Inbox.
>
> If you're using another email provider or a self-hosted mail server, use the credentials required by that provider.

---

## Usage

Run the application:

```bash
python main.py
```

After logging in, you can:

* Send emails
* Browse your inbox
* Read email contents
* Download attachments

---

## License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

See the [LICENSE](LICENSE) file for the complete license text.
