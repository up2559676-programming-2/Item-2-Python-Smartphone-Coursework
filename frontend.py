from tkinter import (
    Checkbutton,
    Entry,
    Frame,
    IntVar,
    StringVar,
    Tk,
    Label,
    Button,
    Toplevel,
    messagebox,
)

from backend import Smartphone


class SmartphoneGui:
    def __init__(self, smartphone: Smartphone) -> None:
        self.smartphone = smartphone

        self.win = Tk()
        self.win.title("BnL Smartphone")
        self.win.geometry("800x600")

        self.battery_var = StringVar()
        self.battery_saver_var = StringVar()
        self.storage_left_var = StringVar()
        self.num_photos_var = IntVar()
        self.photos_storage_used_var = StringVar()
        self.num_videos_var = IntVar()
        self.videos_storage_used_var = StringVar()

        self.duration_var = StringVar(value="0")
        # self.index_var = StringVar()

        self._refresh()

    def _refresh(self):
        photos_storage_used = self.smartphone.photos_app.calculate_storage_used()
        videos_storage_used = self.smartphone.yourtube_app.calculate_storage_used()

        self.battery_var.set(f"{self.smartphone.battery}%")
        self.battery_saver_var.set(self.smartphone.battery_saver_str)
        self.storage_left_var.set(f"{self.smartphone.storage_left:.2f}GB")
        self.num_photos_var.set(self.smartphone.photos_app.num_photos)
        self.photos_storage_used_var.set(f"{photos_storage_used:.2f}GB")
        self.num_videos_var.set(len(self.smartphone.yourtube_app.videos))
        self.videos_storage_used_var.set(f"{videos_storage_used:.2f}GB")

    def create_widgets(self):
        self._create_smartphone_widgets()
        self._create_photo_app_widgets()
        self._create_yourtube_app_widgets()

    def _create_smartphone_widgets(self):
        Label(self.win, text="BnL Smartphone").pack()

        info_frame = Frame(self.win)
        info_frame.pack()

        Label(info_frame, text="Storage Capacity:").grid(row=0, column=0)
        Label(info_frame, text=self.smartphone.storage_capacity).grid(row=0, column=1)

        Label(info_frame, text="Battery:").grid(row=1, column=0)
        Label(info_frame, textvariable=self.battery_var).grid(row=1, column=1)

        Label(info_frame, text="Battery Saver Mode:").grid(row=2, column=0)
        Label(info_frame, textvariable=self.battery_saver_var).grid(row=2, column=1)

        Label(info_frame, text="Storage Left:").grid(row=3, column=0)
        Label(info_frame, textvariable=self.storage_left_var).grid(row=3, column=1)

        button_frame = Frame(self.win)
        button_frame.pack()

        Button(
            button_frame, text="Toggle Battery Saver", command=self.toggle_battery_saver
        ).grid(row=0, column=0)
        Button(button_frame, text="Charge Battery", command=self.charge_battery).grid(
            row=0, column=1
        )

    def _create_photo_app_widgets(self):
        Label(self.win, text="Photos App").pack()

        photos_frame = Frame(self.win)
        photos_frame.pack()

        Label(photos_frame, text="Number of Photos:").grid(row=0, column=0)
        Label(photos_frame, textvariable=self.num_photos_var).grid(row=0, column=1)

        Label(photos_frame, text="Storage Used:").grid(row=1, column=0)
        Label(photos_frame, textvariable=self.photos_storage_used_var).grid(
            row=1, column=1
        )

        photos_button_frame = Frame(self.win)
        photos_button_frame.pack()

        Button(photos_button_frame, text="Take Photos", command=self.take_photo).grid(
            row=0, column=0
        )
        Button(
            photos_button_frame, text="Delete Photo", command=self.delete_photo
        ).grid(row=0, column=1)

    def _create_yourtube_app_widgets(self):
        Label(self.win, text="YourTube App").pack()

        yourtube_frame = Frame(self.win)
        yourtube_frame.pack()

        Label(yourtube_frame, text="Number of Saved Videos:").grid(row=0, column=0)
        Label(yourtube_frame, textvariable=self.num_videos_var).grid(row=0, column=1)

        Label(yourtube_frame, text="Storage Used:").grid(row=1, column=0)
        Label(yourtube_frame, textvariable=self.videos_storage_used_var).grid(
            row=1, column=1
        )

        save_frame = Frame(self.win)
        save_frame.pack()

        # duration_entry = Entry(save_frame, textvariable=self.duration_var, width=30)
        # duration_entry.insert(0, "Write the duration here")
        # duration_entry.grid(row=0, column=0)
        Button(save_frame, text="Save Video", command=self.open_save_video_window).grid(
            row=0, column=1
        )

        delete_frame = Frame(self.win)
        delete_frame.pack()

        # index_entry = Entry(delete_frame, textvariable=self.index_var, width=30)
        # index_entry.insert(0, "Write the index here")
        # index_entry.grid(row=0, column=0)
        Button(
            delete_frame, text="Delete Video", command=self.open_delete_video_window
        ).grid(row=0, column=1)

    def toggle_battery_saver(self):
        self.smartphone.battery_saver_mode = not self.smartphone.battery_saver_mode
        self._refresh()

    def charge_battery(self):
        self.smartphone.charge_battery()
        self._refresh()

    def take_photo(self):
        try:
            self.smartphone.take_photo()
        except MemoryError:
            ...
        except RuntimeError:
            ...

        self._refresh()

    def delete_photo(self):
        try:
            self.smartphone.delete_photo()
        except ValueError:
            ...
        except RuntimeError:
            ...

        self._refresh()

    def save_video(self, win: Toplevel):
        try:
            dur = int(self.duration_var.get())
            if dur <= 0:
                raise ValueError("Duration must be positive")
            self.smartphone.save_video(dur)
            win.destroy()
            self._refresh()
        except MemoryError as e:
            messagebox.showerror("Storage Full", str(e), parent=win)
        except RuntimeError as e:
            messagebox.showerror("Battery Dead", str(e), parent=win)
        except ValueError:
            messagebox.showerror("Error", "Enter a positive integer.", parent=win)

    def open_save_video_window(self):
        win = Toplevel(self.win)
        win.title("Save Video")
        win.geometry("300x200")

        Label(win, text="Video duration (seconds):").pack()
        Entry(win, textvariable=self.duration_var, width=14, justify="center").pack()

        Button(
            win,
            text="Save",
            command=lambda: self.save_video(win),
            bg="#a6e3a1",
            fg="#1e1e2e",
            font=("Helvetica", 9, "bold"),
            relief="flat",
            padx=8,
        ).pack(pady=10)

    def delete_videos(self, win: Toplevel, button_vars: list[IntVar]):
        if all(var.get() == 0 for var in button_vars):
            messagebox.showwarning("No Selection", "Please select a video.", parent=win)
            return

        for index in reversed(range(len(button_vars))):
            var = button_vars[index]
            if not var.get():
                continue

            print(index)

            try:
                self.smartphone.delete_video(index)
            except RuntimeError as e:
                messagebox.showerror("Battery Dead", str(e), parent=win)

        win.destroy()
        self._refresh()

    def open_delete_video_window(self):
        videos = self.smartphone.yourtube_app.videos
        if not videos:
            messagebox.showwarning("No Videos", "There are no videos to delete.")
            return

        win = Toplevel(self.win)
        win.title("Delete Video")
        win.geometry("320x240")

        Label(win, text="Select a video to delete:").pack()

        button_vars: list[IntVar] = []
        for i, dur in enumerate(videos):
            size_mb = dur * 2

            var = IntVar()
            Checkbutton(
                win, text=f"Video {i + 1}:  {dur}s  ({size_mb} MB)", variable=var
            ).pack()
            button_vars.append(var)

        Button(
            win,
            text="Delete Selected",
            command=lambda: self.delete_videos(win, button_vars),
        ).pack()

    def run(self):
        self.create_widgets()
        self.win.mainloop()


def main():
    smartphone = Smartphone(512)
    gui = SmartphoneGui(smartphone)
    gui.run()


if __name__ == "__main__":
    main()
