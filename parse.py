import email
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime
from bs4 import BeautifulSoup


def decode_payload(part):
    payload = part.get_payload(decode=True)
    if not payload:
        return ""

    charset = part.get_content_charset() or "utf-8"
    return payload.decode(charset, errors="ignore")


def decode_header_value(value):
    if not value:
        return ""

    result = ""
    for text, encoding in decode_header(value):
        if isinstance(text, bytes):
            result += text.decode(encoding or "utf-8", errors="ignore")
        else:
            result += text
    return result


def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "head", "title", "meta"]):
        tag.decompose()

    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            link.append(f" ({href})")

    text = soup.get_text(separator="\n")

    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    return "\n".join(lines)


def parse(mail_id, mode, imap):
    status, data = imap.fetch(mail_id, "(RFC822)")
    if status != "OK":
        print("Failed to retrieve email.")
        return

    msg = email.message_from_bytes(data[0][1])

    name, email_addr = parseaddr(msg.get("From"))
    sender = decode_header_value(name)
    subject = decode_header_value(msg.get("Subject"))

    dt = parsedate_to_datetime(msg.get("Date")).astimezone()
    formatted_date = dt.strftime("%a, %d %b %Y %I:%M %p")

    # Inbox preview
    if mode == 0:
        print(f"[{int(mail_id)}]")
        print(f"    From    : {sender}")
        print(f"    Date    : {formatted_date}")
        print(f"    Subject : {subject}\n")
        return

    body = ""
    html_body = ""
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():

            disposition = part.get_content_disposition()
            filename = part.get_filename()

            if disposition == "attachment" and filename:
                attachments.append((decode_header_value(filename), part))
                continue

            ctype = part.get_content_type()

            if ctype == "text/plain" and not body:
                text = decode_payload(part)
                if text.strip():
                    body = text

            elif ctype == "text/html" and not html_body:
                html = decode_payload(part)
                if html.strip():
                    html_body = html

    else:
        if msg.get_content_type() == "text/plain":
            body = decode_payload(msg)
        elif msg.get_content_type() == "text/html":
            html_body = decode_payload(msg)

    if not body and html_body:
        body = html_to_text(html_body)

    # -------- Display email --------

    print(f"Mail ID : {int(mail_id)}")
    print(f"From    : {sender} <{email_addr}>")
    print(f"To      : {msg.get('To')}")
    print(f"Date    : {formatted_date}")
    print(f"Subject : {subject}")

    print("\n" + "=" * 80)
    print("Body:\n")
    print(body if body else "[No message body]")
    print("=" * 80)

    # -------- Attachments --------

    if attachments:
        print("\nAttachments:")
        for i, (filename, _) in enumerate(attachments, start=1):
            print(f"  {i}. {filename}")

        choice = input(
            "\nDownload attachment(s)? "
            "(numbers separated by commas or Enter to skip): "
        ).strip()

        if choice:
            try:
                for idx in [int(x.strip()) - 1 for x in choice.split(",")]:
                    if 0 <= idx < len(attachments):
                        filename, part = attachments[idx]

                        with open(filename, "wb") as f:
                            f.write(part.get_payload(decode=True))

                        print(f"Downloaded: {filename}")

            except ValueError:
                print("Invalid selection.")