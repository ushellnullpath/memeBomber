'''
Project: memeBomber
By: ushellnullpath
Description: memeBomber application's main functions
Last updated on (D/M/Y): 23/01/2024
'''

import os
import praw
import prawcore
import requests
from urllib.parse import urlparse, unquote
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import datetime


def download_meme(client_id, client_secret, user_agent, subreddit_name):
    """
    Download a meme from the specified subreddit.

    Parameters:
    - client_id (str): Reddit API client ID.
    - client_secret (str): Reddit API client secret.
    - user_agent (str): User agent string for Reddit API.
    - subreddit_name (str): Name of the subreddit to fetch memes from.

    Returns:
    - tuple or None: A tuple containing the file path, post information, and unique filename if successful, None otherwise.
    """
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent)

        sub_reddit = reddit.subreddit(subreddit_name)
        post = sub_reddit.new(limit=1).__next__()

        url = post.url

        # check if the URL ends with a common image file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        parsed_url = urlparse(url)
        _, file_extension = os.path.splitext(parsed_url.path)
        file_extension = unquote(file_extension).lower()

        if file_extension not in valid_extensions:
            print(
                f"Invalid file extension! Skipping download.")
            return None

        file_name = os.path.basename(parsed_url.path)

        # create a 'memes' folder if it doesn't exist
        folder_path = "memes"
        os.makedirs(folder_path, exist_ok=True)

        # delete old meme files in the 'memes' folder
        for old_file in [f for f in os.listdir(folder_path) if f.endswith(tuple(valid_extensions))]:
            old_file_path = os.path.join(folder_path, old_file)
            try:
                os.unlink(old_file_path)
            except Exception as e:
                print(f"Error deleting old file {old_file_path}: {e}")

        # download the meme
        try:
            r = requests.get(url)
            r.raise_for_status()  # raising an HTTP Error for bad responses

            # unique filename var for the meme
            unique_filename = f"{file_name}"
            meme_file_path = os.path.join(folder_path, unique_filename)

            # save the file
            with open(meme_file_path, "wb") as f:
                f.write(r.content)

            # save meme details to a JSON file
            post_info = {
                "title": str(post.title),
                "author": str(post.author),
                "url": str(post.url),
            }

            with open(os.path.join(folder_path, "post_info.json"), "w", encoding="utf-8") as info_file:
                json.dump(post_info, info_file, indent=2, ensure_ascii=False)

            return meme_file_path, post_info, unique_filename

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")

    except prawcore.exceptions.PrawcoreException as reddit_err:
        print(f"Reddit API Exception: {reddit_err}")

    return None


def send_meme(email_from, email_password, email_to, post_info, meme_file_path):
    """
    Send a meme via email.

    Parameters:
    - email_from (str): Sender's email address.
    - email_password (str): Sender's email password.
    - email_to (str): Recipient's email address.
    - post_info (dict): Information about the Reddit post.
    - meme_file_path (str): File path of the downloaded meme.
    """

    # setup port number and server name
    smtp_port = 587  # standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # OR/ your mail provider's SMTP server

    # read the content of the JSON file
    json_content = post_info

    # create a string representation of the JSON content for the email body
    json_body = json.dumps(json_content, indent=2, ensure_ascii=False).encode(
        'utf-8').decode('utf-8')
    json_body = json_body.replace('{', '').replace(
        '}', '').replace('"', '').replace(',', '')

    # add the JSON content to the email body with an embedded image
    body = f"""
    <html>
      <body>
        <img src="cid:image_attachment_cid">
        <pre>{json_body}</pre>
      </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to

    # attach the body of the message
    msg.attach(MIMEText(body, 'html'))

    # define the image file to embed
    image_filename = meme_file_path

    # open the image file in binary mode
    with open(image_filename, 'rb') as image_file:
        # create a MIME image object
        image_attachment = MIMEImage(image_file.read())
        # generate a unique Content-ID for the image
        image_attachment.add_header('Content-ID', '<image_attachment_cid>')
        # set the inline disposition
        image_attachment.add_header(
            'Content-Disposition', 'inline', filename=image_filename)

    # attach the image to the email body
    msg.attach(image_attachment)

    # cast the email message to a string
    text = msg.as_string()

    # connect to the server and send the email
    try:
        print("\nConnecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, email_password)
        print("Connected to server.")

        print(f"Sending email to -> {email_to}")
        TIE_server.sendmail(email_from, email_to, text)
        print(f"Email successfully sent to -> {email_to}")
        timestamp = datetime.datetime.now().strftime("%I:%M:%S %p")
        print(f"Sent at: {timestamp}\n")

    except Exception as e:
        print(f"Error sending email: {e}")

    finally:
        TIE_server.quit()


def bombing_process(client_id, client_secret, user_agent, subreddit_name, email_from, email_password, email_to):
    """
    Execute the main meme bombing process.

    Parameters:
    - client_id (str): Reddit API client ID.
    - client_secret (str): Reddit API client secret.
    - user_agent (str): User agent string for Reddit API.
    - subreddit_name (str): Name of the subreddit to fetch memes from.
    - email_from (str): Sender's email address.
    - email_password (str): Sender's email password.
    - email_to (str): Recipient's email address.
    """

    # download the meme and get the necessary information
    download_result = download_meme(
        client_id, client_secret, user_agent, subreddit_name)

    if download_result:
        meme_file_path, post_info, _ = download_result

        # send the meme with the obtained information
        send_meme(email_from, email_password, email_to,
                  post_info, meme_file_path)
    else:
        print("Error downloading meme.")
