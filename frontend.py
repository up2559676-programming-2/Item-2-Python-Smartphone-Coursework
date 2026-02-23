from tkinter import Entry, Frame, StringVar, Tk, Label, Button


class SmartphoneGui:
    def __init__(self) -> None:
        self.win = Tk()
        self.win.title("BnL Smartphone")
        self.win.geometry("800x600")

        self.duration_var = StringVar()
        self.index_var = StringVar()

    def create_widgets(self):
        self._create_smartphone_widgets()
        self._create_photo_app_widgets()
        self._create_yourtube_app_widgets()

    def _create_smartphone_widgets(self):
        Label(self.win, text="BnL Smartphone").pack()

        info_frame = Frame(self.win)
        info_frame.pack()

        Label(info_frame, text="Storage Capacity:").grid(row=0, column=0)
        Label(info_frame, text="512GB").grid(row=0, column=1)

        Label(info_frame, text="Battery:").grid(row=1, column=0)
        Label(info_frame, text="75%").grid(row=1, column=1)

        Label(info_frame, text="Battery Saver Mode:").grid(row=2, column=0)
        Label(info_frame, text="Disabled").grid(row=2, column=1)

        Label(info_frame, text="Storage Left:").grid(row=3, column=0)
        Label(info_frame, text="500GB").grid(row=3, column=1)

        button_frame = Frame(self.win)
        button_frame.pack()

        Button(button_frame, text="Toggle Battery Saver").grid(row=0, column=0)
        Button(button_frame, text="Charge Battery").grid(row=0, column=1)

    def _create_photo_app_widgets(self):
        Label(self.win, text="Photos App").pack()

        photos_frame = Label(self.win)
        photos_frame.pack()

        Label(photos_frame, text="Number of Photos:").grid(row=0, column=0)
        Label(photos_frame, text="42").grid(row=0, column=1)

        Label(photos_frame, text="Storage Used:").grid(row=1, column=0)
        Label(photos_frame, text="10GB").grid(row=1, column=1)

        photos_button_frame = Frame(self.win)
        Button(photos_button_frame, text="Take Photos").grid(row=0, column=0)
        Button(photos_button_frame, text="Delete Photo").grid(row=0, column=1)

    def _create_yourtube_app_widgets(self):
        Label(self.win, text="YourTube App").pack()

        yourtube_frame = Frame(self.win)
        yourtube_frame.pack()

        Label(yourtube_frame, text="Number of Saved Videos:").grid(row=0, column=0)
        Label(yourtube_frame, text="4").grid(row=0, column=1)

        Label(yourtube_frame, text="Storage Used:").grid(row=1, column=0)
        Label(yourtube_frame, text="1.25GB").grid(row=1, column=1)

        save_frame = Frame(self.win)
        save_frame.pack()

        Entry(save_frame, textvariable=self.duration_var, width=30).grid(
            row=0, column=0
        )
        Button(save_frame, text="Save Video").grid(row=0, column=1)

        delete_frame = Frame(self.win)
        delete_frame.pack()

        Entry(delete_frame, textvariable=self.index_var, width=30).grid(row=0, column=0)
        Button(delete_frame, text="Delte Video").grid(row=0, column=1)

    def run(self):
        self.create_widgets()
        self.win.mainloop()


def main():
    gui = SmartphoneGui()
    gui.run()


main()
