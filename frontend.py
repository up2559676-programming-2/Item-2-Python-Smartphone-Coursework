import functools
from tkinter import Button, Entry, Frame, Label, StringVar, Tk

from backend import AppGui, Smartphone


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

        Button(button_frame, text="Toggle Battery Saver").grid(row=0, column=0, padx=5)
        Button(button_frame, text="Charge Battery").grid(row=0, column=1, padx=5)

    def _create_photo_app_widgets(self):
        Label(self.win, text="Photos App").pack()

        photos_frame = Frame(self.win)
        photos_frame.pack()

        Label(photos_frame, text="Number of Photos:").grid(row=0, column=0)
        Label(photos_frame, text="42").grid(row=0, column=1)

        Label(photos_frame, text="Storage Used:").grid(row=1, column=0)
        Label(photos_frame, text="10GB").grid(row=1, column=1)

        photos_button_frame = Frame(self.win)
        photos_button_frame.pack()
        Button(photos_button_frame, text="Take Photos").grid(row=0, column=0, padx=5)
        Button(photos_button_frame, text="Delete Photo").grid(row=0, column=1, padx=5)

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
            row=0, column=0, padx=5
        )
        Button(save_frame, text="Save Video").grid(row=0, column=1, padx=5)

        delete_frame = Frame(self.win)
        delete_frame.pack()

        Entry(delete_frame, textvariable=self.index_var, width=30).grid(
            row=0, column=0, padx=5
        )
        Button(delete_frame, text="Delete Video").grid(row=0, column=1, padx=5)

    def run(self):
        self.create_widgets()
        self.win.mainloop()


class SmartphoneGuiTask6(SmartphoneGui):
    def __init__(self, smartphone: Smartphone) -> None:
        self.smartphone = smartphone

        self.win = Tk()
        self.win.title("BnL Smartphone")
        self.win.geometry("800x600")

        self.battery_var = StringVar()
        self.battery_saver_var = StringVar()
        self.storage_left_var = StringVar()

        self.app_buttons: list[Button] = []
        self._refresh()

    def _refresh(self):
        self.battery_var.set(f"{self.smartphone.battery}%")
        self.battery_saver_var.set(self.smartphone.battery_saver_str)
        self.storage_left_var.set(f"{self.smartphone.storage_left:.2f}GB")

        battery_empty = self.smartphone.battery == 0

        for btn in self.app_buttons:
            btn.config(state="disabled" if battery_empty else "normal")

    def _create_smartphone_widgets(self):
        Label(self.win, text="BnL Smartphone").pack(pady=(0, 20))

        info_frame = Frame(self.win)
        info_frame.pack()

        Label(info_frame, text="Storage Capacity:").grid(row=0, column=0)
        Label(info_frame, text=f"{self.smartphone.storage_capacity}GB").grid(
            row=0, column=1
        )

        Label(info_frame, text="Battery:").grid(row=1, column=0)
        Label(info_frame, textvariable=self.battery_var).grid(row=1, column=1)

        Label(info_frame, text="Battery Saver Mode:").grid(row=2, column=0)
        Label(info_frame, textvariable=self.battery_saver_var).grid(row=2, column=1)

        Label(info_frame, text="Storage Left:").grid(row=3, column=0)
        Label(info_frame, textvariable=self.storage_left_var).grid(row=3, column=1)

        button_frame = Frame(self.win)
        button_frame.pack(pady=(0, 20))

        Button(
            button_frame, text="Toggle Battery Saver", command=self.toggle_battery_saver
        ).grid(row=0, column=0, padx=5)

        Button(button_frame, text="Charge Battery", command=self.charge_battery).grid(
            row=0, column=1, padx=5
        )

        apps_frame = Frame(self.win)
        apps_frame.pack()
        for i, app in enumerate(self.smartphone.apps):
            btn = Button(
                apps_frame,
                text=app.APP_NAME,
                command=functools.partial(self.open_app, app),
                width=15,
                height=5,
            )
            btn.grid(row=i, column=0)
            self.app_buttons.append(btn)

    def create_widgets(self):
        self._create_smartphone_widgets()

    def open_app(self, app: AppGui):
        app_win = app.render(self.smartphone)
        self.win.wait_window(app_win)
        self._refresh()

    def toggle_battery_saver(self):
        self.smartphone.battery_saver_mode = not self.smartphone.battery_saver_mode
        self._refresh()

    def charge_battery(self):
        self.smartphone.charge_battery()
        self._refresh()


def main():
    gui = SmartphoneGui()
    gui.run()
    smartphone = Smartphone(512)
    smartphone.battery = 10
    gui_task6 = SmartphoneGuiTask6(smartphone)
    gui_task6.run()


if __name__ == "__main__":
    main()
