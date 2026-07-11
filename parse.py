import email
import os
from email.utils import parseaddr, parsedate_to_datetime
from email.header import decode_header


def decode_payload(part):
    payload = part.get_payload(decode=True)
    if payload:
        return payload.decode(
            part.get_content_charset() or "utf-8",
            errors="ignore"
        )
    return ""


def parse(mail_id, x, imap):
    stat, data = imap.fetch(mail_id, "(RFC822)")

    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    # Decode sender name
    name, email_addr = parseaddr(msg["From"])
    decoded_name = ""
    for part, enc in decode_header(name):
        decoded_name += part.decode(enc or "utf-8") if isinstance(part, bytes) else part

    # Decode subject
    subject = ""
    for part, enc in decode_header(msg["Subject"]):
        subject += part.decode(enc or "utf-8") if isinstance(part, bytes) else part

    # Format date
    dt = parsedate_to_datetime(msg["Date"]).astimezone()
    formatted_date = dt.strftime("%a, %d %b %Y %I:%M %p")

    # Summary view
    if x == 0:
        print(f"[{int(mail_id)}]")
        print(f"    From    : {decoded_name}")
        print(f"    Date    : {formatted_date}")
        print(f"    Subject : {subject}\n")

    # Detailed view
    elif x == 1:

        body = ""
        attachments = []

        if msg.is_multipart():
            for part in msg.walk():

                filename = part.get_filename()
                if filename:
                    attachments.append(filename)

                disposition = str(part.get("Content-Disposition"))
                if "attachment" in disposition.lower():
                    continue

                if part.get_content_type() == "text/plain":
                    body = decode_payload(part)
                    if body:
                        break

            if not body:
                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        body = decode_payload(part)
                        if body:
                            break

        else:
            body = decode_payload(msg)

        print(f"Mail ID : {int(mail_id)}")
        print(f"From    : {decoded_name} <{email_addr}>")
        print(f"To      : {msg['To']}")
        print(f"Date    : {formatted_date}")
        print(f"Subject : {subject}")

        if attachments:
            print("\nAttachments:")
            for file in attachments:
                print(f"  - {file}")

        print("\nBody:\n")
        print(body)