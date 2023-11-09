"""
This module contains functions for sending random beats via email.
"""

import argparse
import os
import random
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv


def send_files(email_address: str, directory: str, num_files: int):
    """
    Sends n random files from the specified directory to the specified email address.

    Args:
    - directory (str): The directory to get the files from.
    - email_address (str): The email address to send the files to.
    - n (int): The number of files to send.

    Returns:
    - None
    """
    load_dotenv()
    sender_email_address = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("PASSWORD")
    if sender_email_address is None or password is None:
        raise ValueError("Email address and password must be set as environment variables")

    files = os.listdir(directory)
    mp3_files = [file for file in files if file.endswith(".mp3")]
    if len(mp3_files) < num_files:
        raise ValueError(
            f"{num_files} mp3 files requested but there are only {len(mp3_files)} in the directory"
        )

    msg: MIMEMultipart = MIMEMultipart()
    msg["From"] = sender_email_address
    msg["To"] = email_address
    msg["Subject"] = "beats"

    # TODO: Support freezing files and refreshing the non-frozen files

    while True:
        # choose a new set of files
        chosen_files = random.sample(mp3_files, num_files)

        # make sure that size is below 25Mb limit
        total_size = 0
        files_too_big = False
        for file in chosen_files:
            file_path = os.path.join(directory, file)
            total_size += os.path.getsize(file_path)
            if total_size > 25 * 1024 * 1024:
                files_too_big = True
                break
        if files_too_big:
            continue

        # Confirm that the user wants to send these files
        print("Files:")
        for file in chosen_files:
            print(file)
        print(
            f"\nSend these {num_files} beats to {email_address}? (y [send] / n [new beats])",
            end=" ",
        )
        while True:
            response = input().lower()
            if response == "y" or response == "n":
                break
        if response == "n":
            print("\n")
            continue

        # Add the files to the email
        for file in chosen_files:
            part: MIMEBase = MIMEBase("application", "octet-stream")
            part.set_payload(open(os.path.join(directory, file), "rb").read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", f"attachment; filename={os.path.basename(file)}"
            )
            msg.attach(part)
        break

    print("Sending email...")
    server: smtplib.SMTP = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email_address, password)
    server.send_message(msg)
    server.quit()

    print("Email sent successfully")


def main():
    """
    Sends a number of beat files from a directory to an email address.

    Required arguments:
    --email_address (-e): Email address to send beats to.

    Optional arguments:
    --directory (-d): Directory to get beats from. Defaults to current directory.
    --num_files (-n): Number of beats to send. Defaults to 5.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--email_address",
        "-e",
        type=str,
        required=True,
        help="Email address to send beats to (required)",
    )
    parser.add_argument(
        "--directory",
        "-d",
        type=str,
        required=False,
        default=".",
        help="Directory to get beats from (defaults to current directory)",
    )
    parser.add_argument(
        "--num_files",
        "-n",
        type=int,
        required=False,
        default=5,
        help="Number of beats to send (defaults to 5)",
    )
    args = parser.parse_args()

    send_files(args.email_address, args.directory, args.num_files)


if __name__ == "__main__":
    main()
