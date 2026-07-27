import os
import time
import getpass
import imaplib
import smtplib

import viewmail
import sendmail


logged = False


def clear():
    os.system("cls" if os.name == "nt" else "clear")


while True:
    clear()

    while not logged:
        clear()

        choice = input(
            "1. Log In\n"
            "2. Quit\n"
            ">> "
        )

        if choice == "1":

            clear()

            provider = input(
                "Choose provider:\n"
                "1. Gmail\n"
                "2. Custom Server\n"
                ">> "
            )

            clear()

            if provider == "1":
                imap_server = "imap.gmail.com"
                smtp_server = "smtp.gmail.com"
                smtp_port = 587

            elif provider == "2":
                imap_server = input("IMAP Server: ")
                smtp_server = input("SMTP Server: ")

                try:
                    smtp_port = int(input("SMTP Port: "))
                except ValueError:
                    print("Invalid port.")
                    time.sleep(1)
                    continue

            else:
                print("Invalid choice.")
                time.sleep(1)
                continue

            email_id = input("Email: ")
            password = getpass.getpass("Password: ")

            imap = None
            smtp = None

            try:
                # IMAP
                imap = imaplib.IMAP4_SSL(imap_server, timeout=10)
                imap.login(email_id, password)

                # SMTP
                smtp = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(email_id, password)

                logged = True

                print("Login successful.")
                time.sleep(1)

            except imaplib.IMAP4.error:
                print("IMAP authentication failed.")

            except smtplib.SMTPAuthenticationError:
                print("SMTP authentication failed.")

            except smtplib.SMTPHeloError:
                print("SMTP HELO/EHLO failed.")

            except smtplib.SMTPNotSupportedError:
                print("SMTP AUTH not supported.")

            except smtplib.SMTPException as e:
                print(f"SMTP error: {e}")

            except Exception as e:
                print(f"Login failed: {e}")

            finally:
                if not logged:
                    if imap:
                        try:
                            imap.logout()
                        except:
                            pass

                    if smtp:
                        try:
                            smtp.quit()
                        except:
                            pass

                    time.sleep(1)

        elif choice == "2":
            exit()

        else:
            print("Invalid choice.")
            time.sleep(1)

    # ---------------- Logged In ----------------

    while logged:

        clear()

        service = input(
            "1. Send Mail\n"
            "2. View Mails\n"
            "3. Logout\n"
            "4. Quit\n"
            ">> "
        )

        if service == "1":
            clear()
            sendmail.send(smtp, email_id)
            input("\nPress Enter to continue...")

        elif service == "2":
            viewmail.view(imap)

        elif service == "3":

            try:
                imap.logout()
            except:
                pass

            try:
                smtp.quit()
            except:
                pass

            logged = False

        elif service == "4":

            try:
                imap.logout()
            except:
                pass

            try:
                smtp.quit()
            except:
                pass

            exit()

        else:
            print("Invalid choice.")
            time.sleep(1)