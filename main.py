'''
Project: memeBomber
By: ushellnullpath
Description:
A simple app for sending meme-filled emails using the Reddit API. 
It fetches memes from a specified subreddit and sends them via email.
Last updated on (D/M/Y): 23/01/2024
'''

import os
from customtkinter import *
from PIL import Image
from functions import bombing_process
from CTkMessagebox import CTkMessagebox
from dotenv import load_dotenv
import webbrowser
import random
import time


class memeBomber():
    def __init__(self):
        # loads environment variables from a .env file, allowing overrides if existing variables
        load_dotenv(override=True)

        # reddit API
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = "memeBomber by ushellnullpath"
        self.subreddit_name = "memes"

        # email configuration
        self.email_from = os.getenv("EMAIL_ADDRESS")
        self.email_password = os.getenv("EMAIL_PASSWORD")

        # variables
        self.bombing = False
        self.explode_labels = []
        self.timer_running = False
        self.timer_duration = 180  # 3 minutes in sec
        self.remaining_time = self.timer_duration
        self.bombing_scheduled = False

        self.create_gui()

    def create_gui(self):
        """
        Create the graphical user interface for the application.
        """

        def win_move(event):
            """
            Handle GUI's window movement.
            """
            x, y = self.root.winfo_pointerxy()
            self.root.geometry(f"+{x}+{y}")

        self.root = CTk()
        self.root.title("memeBomber by ushellnullpath")
        self.width_of_win = 530
        self.height_of_win = 710
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x_coord = ((self.screen_width//2) - (self.width_of_win//2))
        self.y_coord = ((self.screen_height//2) - (self.height_of_win//2))
        self.root.geometry(("%dx%d+%d+%d") %
                           (self.width_of_win, self.height_of_win, self.x_coord, self.y_coord))

        self.root.configure(fg_color="#ffffff")
        self.root._set_appearance_mode("light")
        self.root.attributes('-topmost', True)
        self.root.bind('<B1-Motion>', win_move)
        self.root.overrideredirect(True)

        self.logo_symbol = CTkImage(Image.open(
            "images\logo1.png"), size=(531, 509))
        self.logo_screen = CTkLabel(master=self.root, image=self.logo_symbol,
                                    fg_color="#ffffff", text=None)
        self.logo_screen.place(relx=0.5, rely=0.385, anchor=CENTER)

        self.line = CTkLabel(self.root, width=531,
                             bg_color='#111111', text=None)
        self.line.place(relx=0.5, rely=0, anchor=CENTER)

        self.close_bttn = CTkButton(master=self.root, text="❌", font=(
            "Arial Black", 15, "bold"), text_color="#111111", bg_color="#ffffff", fg_color="#ffffff", hover_color="#ffff00", cursor="hand2", width=1, command=self.root.destroy)
        self.close_bttn.place(relx=0.925, rely=0.0295)

        self.user_frame1 = CTkFrame(master=self.root, width=531, height=148,
                                    corner_radius=0, border_width=0, fg_color="#ffffff")
        self.user_frame1.place(relx=0.5, rely=0.853, anchor=CENTER)

        self.user_frame2 = CTkFrame(master=self.root, width=531, height=148,
                                    corner_radius=0, border_width=0, fg_color="#ffffff")
        self.user_frame2.place(relx=0.5, rely=0.853, anchor=CENTER)

        self.frame1()
        self.frame2()

        self.show_frame(self.user_frame1)

        self.terms_bttn = CTkButton(master=self.root, text="memeBomber Terms", font=(
            "Arial Black", 10, "bold", "underline"), text_color="#111111", fg_color="#ffffff", hover_color="#ffffff", cursor="hand2", width=1, command=self.openlink)
        self.terms_bttn.place(relx=0.50, rely=0.98, anchor=CENTER)

    def run(self):
        """
        Starts the main event loop for the memeBomber application.
        """

        self.root.mainloop()

    def show_frame(self, frame):
        """
        Show the specified frame in the GUI.

        Parameters:
        - frame (CTkFrame): The frame to be displayed.
        """

        frame.tkraise()

    def timer(self):
        if self.timer_running == True:

            # check if the timer_label attribute is not created yet
            if not hasattr(self, 'timer_label') or self.timer_label is None:
                # create a label to display the timer in the frame2
                self.timer_label = CTkLabel(master=self.user_frame2, text="", font=(
                    "Century Gothic", 15), text_color="#ffffff", fg_color="#111111", corner_radius=5)
                self.timer_label.place(relx=0.5, rely=0.46, anchor=CENTER)

            # check if the timer has expired
            if self.remaining_time <= 0:
                # reset the timer when it reaches zero
                self.remaining_time = self.timer_duration

            # display the formatted time in the label
            self.timer_label.configure(
                text=f"{time.strftime('%M:%S', time.gmtime(self.remaining_time))} remaining until the next bombing!")

            # update the remaining time
            self.remaining_time -= 1

            # schedule the function to run after 1 second
            self.root.after(1000, self.timer)

    def openlink(self):
        webbrowser.open(
            "https://github.com/ushellnullpath/memeBomber/blob/main/LICENSE")

    def is_valid_email(self, email):
        return "@" in email and ".com" in email

    def explode_label(self):
        """
        Create and place an explosion label that indicates the instances of the bombing in the GUI.
        """

        x_coord = random.uniform(0.2, 0.8)
        y_coord = random.uniform(0.2, 0.7)

        explode_label = CTkLabel(self.root, text="💥", font=(
            'Arial Black', 14, "bold"), text_color="#ff0000")
        explode_label.place(relx=x_coord, rely=y_coord, anchor=CENTER)

        self.explode_labels.append(explode_label)

    def start_bombing(self):
        if self.bombing:
            return

        if self.entrybox_1e.get() == '':
            CTkMessagebox(
                master=self.root, title="Field is required!", message="You have left a field empty, and a value must be entered.",
                font=('Arial Black', 12), icon="warning", sound=True, button_color="#ffff00", fg_color="#111111", bg_color="#111111",
                button_text_color="#111111", button_hover_color="#ffde00", cancel_button="None")
        elif not self.is_valid_email(self.entrybox_1e.get()):
            CTkMessagebox(
                master=self.root, title="Invalid Email!", message="Please enter a valid email address.", font=('Arial Black', 12),
                icon="warning", sound=True, button_color="#ffff00", fg_color="#111111", bg_color="#111111", button_text_color="#111111",
                button_hover_color="#ffde00", cancel_button="None")
        else:
            # reset remaining time to default duration when starting a new bombing process
            self.remaining_time = self.timer_duration
            CTkMessagebox(
                master=self.root, title="Bombing Started!", message="Your request has been initiated.", font=('Arial Black', 12),
                icon="check", sound=True, button_color="#ffff00", fg_color="#111111", bg_color="#111111", button_text_color="#111111",
                button_hover_color="#ffde00", cancel_button="None")
            self.target_email = self.entrybox_1e.get()

            bombing_process(self.client_id, self.client_secret, self.user_agent,
                            self.subreddit_name, self.email_from, self.email_password, self.target_email)
            self.entrybox_1e.delete(0, END)
            self.show_frame(self.user_frame2)
            self.bombing = True
            self.timer_running = True
            self.timer()
            self.explode_label()
            self.bombing_scheduled = True
            self.schedule_bombing()  # schedule the next bombing process

    def schedule_bombing(self):
        # call the bombing_process function and schedule the next call
        if self.bombing_scheduled == True:

            if self.bombing == True and self.timer_running == True and self.remaining_time <= 0:
                # call the functions only when the timer reaches 3 minutes
                print("Sending another one...")
                self.explode_label()
                bombing_process(self.client_id, self.client_secret, self.user_agent,
                                self.subreddit_name, self.email_from, self.email_password, self.target_email)

            # schedule the next bombing process
            self.root.after(1000, self.schedule_bombing)

    def stop_bombing(self):
        self.bombing = False
        self.timer_running = False
        self.bombing_scheduled = False

        # remove all instances of the explode label
        for label in self.explode_labels:
            label.destroy()

        # clear the list of explosion labels
        self.explode_labels = []

        self.show_frame(self.user_frame1)

    def frame1(self):
        """
        Set up and return the first frame of the GUI before the meme bombing process.

        Returns:
        - CTkFrame: The first frame of the GUI.
        """

        self.label_1 = CTkLabel(master=self.user_frame1, text="Enter Your Victim's Information", font=(
            "Arial Black", 20, 'bold'), text_color="#111111", fg_color="#ffffff")
        self.label_1.place(relx=0.5, rely=0.15, anchor=CENTER)

        self.entrybox_1e = CTkEntry(master=self.user_frame1, width=245, height=35, font=(
            "Century Gothic", 15), placeholder_text="Email", fg_color="#111111", state=NORMAL)
        self.entrybox_1e.place(relx=0.5, rely=0.47, anchor=CENTER)

        self.bomb_bttn_main = CTkButton(master=self.user_frame1, width=184, height=40, text="💣", font=(
            "Arial Black", 20, "bold"), text_color="#111111", bg_color="#ffffff", fg_color="#ffff00", hover_color="#ffde00", cursor="hand2", corner_radius=6, command=self.start_bombing)
        self.bomb_bttn_main.place(relx=0.62, rely=0.8, anchor=E)

        self.stop_bttn_main = CTkButton(master=self.user_frame1, width=49, height=40, text="⏹️", font=(
            "Arial Black", 20, "bold"), text_color="#ffffff", bg_color="#ffffff", fg_color="#ff0000", hover_color="#d10000", corner_radius=6, state=DISABLED)
        self.stop_bttn_main.place(relx=0.64, rely=0.8, anchor=W)

        return self.user_frame1

    def frame2(self):
        """
        Set up and return the second frame of the GUI during the meme bombing process.

        Returns:
        - CTkFrame: The second frame of the GUI.
        """

        self.label_1 = CTkLabel(master=self.user_frame2, text="Your Victim is getting BOMBED!", font=(
            "Arial Black", 20, 'bold'), text_color="#111111", fg_color="#ffffff")
        self.label_1.place(relx=0.5, rely=0.15, anchor=CENTER)

        self.bomb_bttn_main = CTkButton(master=self.user_frame2, width=184, height=40, text="💣", font=(
            "Arial Black", 20, "bold"), text_color="#111111", bg_color="#ffffff", fg_color="#ffff00", hover_color="#ffde00", corner_radius=6, state=DISABLED)
        self.bomb_bttn_main.place(relx=0.62, rely=0.8, anchor=E)

        self.stop_bttn_main = CTkButton(master=self.user_frame2, width=49, height=40, text="⏹️", font=(
            "Arial Black", 20, "bold"), text_color="#ffffff", bg_color="#ffffff", fg_color="#ff0000", hover_color="#d10000", cursor="hand2", corner_radius=6, command=self.stop_bombing)
        self.stop_bttn_main.place(relx=0.64, rely=0.8, anchor=W)

        return self.user_frame2


if __name__ == "__main__":
    App = memeBomber()
    App.run()
