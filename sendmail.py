from email.message import EmailMessage
import mimetypes
import os


def send(smtp, sender):
    recipient = input("To: ").strip()

    subject = input("Subject: ")

    print("Enter message body.")
    print("Type a single '.' on a new line to finish.\n")

    lines = []
    while True:
        line = input()
        if line == ".":
            break
        lines.append(line)

    body = "\n".join(lines)

    msg = EmailMessage()

    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    while True:
        choice = input("Attach a file? (y/n): ").strip().lower()

        if choice != "y":
            break

        path = input("File path: ").strip()

        if not os.path.isfile(path):
            print("File not found.")
            continue

        mime_type, _ = mimetypes.guess_type(path)

        if mime_type:
            maintype, subtype = mime_type.split("/", 1)
        else:
            maintype, subtype = "application", "octet-stream"

        with open(path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype=maintype,
                subtype=subtype,
                filename=os.path.basename(path),
            )

    try:
        smtp.send_message(msg)
        print("Email sent successfully.")

    except Exception as e:
        print(f"Failed to send email: {e}")