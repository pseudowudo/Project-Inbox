import os
import imaplib
from getpass import getpass
from parse import parse


imap_server = "imap.gmail.com"

email_id = input("Enter your email: ")
password = getpass("Enter your password: ")

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_id, password)

os.system("cls" if os.name == "nt" else "clear")

imap.select("INBOX")
_, msgnum = imap.search(None, "ALL")
mail_ids = msgnum[0].split()

page = 0
per_page = 10


while True:
    os.system("cls" if os.name == "nt" else "clear")

    total_pages = (len(mail_ids) - 1) // per_page + 1

    start = len(mail_ids) - ((page + 1) * per_page)
    end = len(mail_ids) - (page * per_page)

    if start < 0:
        start = 0

    current_mails = mail_ids[start:end]

    print("=" * 100)
    print(f"   Inbox   | Page {page + 1}/{total_pages}")
    print("=" * 100)

    for i, mail_id in enumerate(reversed(current_mails), start=1):
        print(f"{i}. ", end="")
        parse(mail_id, 0, imap)

    print()
    print("=" * 50)
    print("n : next page")
    print("p : previous page")
    print("0 : exit")

    choice = input("Open email / command: ")

    if choice == "0":
        break

    elif choice.lower() == "n":
        if page < total_pages - 1:
            page += 1
        else:
            input("Already at last page. Press Enter...")
            
    elif choice.lower() == "p":
        if page > 0:
            page -= 1
        else:
            input("Already at first page. Press Enter...")

    elif choice.isdigit():
        choice = int(choice)

        if 1 <= choice <= len(current_mails):
            selected = list(reversed(current_mails))[choice - 1]

            while True:
                os.system("cls" if os.name == "nt" else "clear")

                parse(selected, 1, imap)

                print("\n" + "=" * 50)
                print("v : back to inbox")
                print("0 : exit")

                action = input("What next? ")

                if action.lower() == "v":
                    break

                elif action == "0":
                    imap.logout()
                    exit()

        else:
            input("Invalid email number. Press Enter...")


imap.logout()