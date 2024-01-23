Been into memes lately, must be because I've been unemployed for quite a while now. In an effort to make productive use of my time, I decided to develop a simple application. memeBomber is a user-friendly GUI application designed for individuals to playfully spam their friends or loved ones with a regular influx of the latest memes delivered directly to their inbox every 3 minutes (modifiable, of course :P). It uses the Reddit API to fetch memes from a specified subreddit (r/memes) and sends them via email.

The UI

The UI when initialized; an "explode" label signifies the number of instances of the "bombing" that have occurred, alongside a timer tracking when the next "bombing" is scheduled.

The program simultaneously creates, stores, and deletes the downloaded image file and post information in a JSON format within the "memes" folder.

Features

    - Email Bombing: Send a series of memes to a specified email address.
    - Customizable Timer: Set a timer to control the frequency of meme bombings.
    - GUI Interface: User-friendly graphical interface for easy interaction.
    - Error Handling and Status: Users can receive error-handled and status print messages
      in their command line interface when running the program for hours.

- LAST UPDATED (D/M/Y): 23/01/2024

Libraries Used:

    os
    praw
    prawcore
    requests
    urllib.parse
    json
    smtplib
    email.mime
    customtkinter
    pillow
    CTkMessagebox
    webbrowser
    random
    time
    datetime

CREDITS: [r/memes](https://www.reddit.com/r/memes/).

DISCLAIMER: This program is released under a MIT License, intended for everyone to enjoy and potentially modify. It's meant to be a fun project, and you are encouraged to add additional features to it or use it as a reference for other programs. However, please note that any use of the program for malicious purposes is not the responsibility of the author, and such usage is strongly discouraged.
