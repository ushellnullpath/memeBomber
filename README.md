Been into memes lately, must be because I've been unemployed for quite a while now. In an effort to make productive use of my time, I decided to develop a simple application. memeBomber is a user-friendly GUI application designed for individuals to playfully spam their friends or loved ones with a regular influx of the latest memes delivered directly to their inbox every 3 minutes (modifiable, of course :P). It uses the Reddit API to fetch memes from a specified subreddit (r/memes) and sends them via email.

The UI

![298813098-f3d224ab-542c-468e-bbac-71eecb4ba030](https://github.com/ushellnullpath/memeBomber/assets/104400332/618db103-5d32-4987-a060-025a9a4a2c07)

The UI when initialized; an "explode" label signifies the number of instances of the "bombing" that have occurred, alongside a timer tracking when the next "bombing" is scheduled.

![298813119-70aefed5-c6bc-4227-adac-1550894276ab](https://github.com/ushellnullpath/memeBomber/assets/104400332/84250326-fcaf-496e-8027-f022c5edde97)

The program simultaneously creates, stores, and deletes the downloaded image file and post information in a JSON format within the "memes" folder.

![298813140-86882bbd-90a6-43cf-b4f4-d5dcc1836036](https://github.com/ushellnullpath/memeBomber/assets/104400332/5afa0b60-8b5f-484b-bfef-b066aaadf248)

Features

    - Email Bombing: Send a series of memes to a specified email address.
    - Customizable Timer: Set a timer to control the frequency of meme bombings.
    - GUI Interface: User-friendly graphical interface for easy interaction.
    - Error Handling and Status: Users can receive error-handled and status print messages
      in their command line interface when running the program for hours.

HOW TO USE

    - In the main.py file; set "self.client_id" and "self.client_secret" (line 27 and 28) to your own Reddit client ID and client secret, which you must create directly on Reddit.
    - In the main.py file; set "self.email_from" and "self.email_password" (line 33 and 34) to the email address and its password, as that account will be used to send the memes.
    - Note: It is better to create a separate '.env' file to store this information. If you do, please set the variable names as REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, EMAIL_ADDRESS, and EMAIL_PASSWORD.

- LAST UPDATED (D/M/Y): 15/06/2024

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
