from tkinter import IntVar, StringVar, Toplevel, Label, Button, Frame


class Smartphone:
    def __init__(self, storage_capacity: int) -> None:
        if storage_capacity <= 0:
            storage_capacity = 256

        self.storage_capacity = storage_capacity
        self.battery: int = 100
        self.battery_saver_mode: bool = False
        self.apps: tuple[PhotosApp, YourTubeApp] = (PhotosApp(self), YourTubeApp(self))

    def __str__(self) -> str:
        return f"BnL Smartphone - Storage: {self.storage_capacity}GB, Battery: {self.battery}%, Battery Saver Mode: {self.battery_saver_str}"

    @property
    def _storage_capacity_mb(self) -> int:
        return self.storage_capacity * 1024

    @property
    def battery_saver_str(self) -> str:
        return "Enabled" if self.battery_saver_mode else "Disabled"

    @property
    def _storage_left_mb(self) -> float:
        return self._storage_capacity_mb - self.total_storage_used_mb()

    @property
    def storage_left(self) -> float:
        return self._storage_left_mb / 1024

    def use_battery(self, amount: int):
        self.battery = max(0, self.battery - amount)

    def charge_battery(self):
        if self.battery_saver_mode:
            self.battery = max(80, self.battery)
        else:
            self.battery = 100

    def _consume_app_usage(self):
        if self.battery <= 0:
            raise RuntimeError("Battery is empty")

        self.use_battery(2)

    def total_storage_used_mb(self) -> float:
        return sum(app.calculate_storage_used_mb() for app in self.apps)

    def _check_storage_available(self, additional_storage: float):
        if (
            self.total_storage_used_mb() + additional_storage
            > self._storage_capacity_mb
        ):
            raise MemoryError("Not enough storage available")

    # def take_photo(self):
    #     self._consume_app_usage()
    #     self._check_storage_available(24)
    #
    #     self.photos_app.take_photo()
    #
    # def delete_photo(self):
    #     self._consume_app_usage()
    #     if self.photos_app.num_photos == 0:
    #         raise ValueError("No photos to delete")
    #
    #     self.photos_app.delete_photo()
    #
    # def save_video(self, duration: int):
    #     self._consume_app_usage()
    #     self._check_storage_available(duration * 2)
    #
    #     self.yourtube_app.save_video(duration)
    #
    # def delete_video(self, index: int):
    #     self._consume_app_usage()
    #     self.yourtube_app.delete_video(index)


class App:
    APP_NAME = "Unnamed App"

    def __init__(self, smartphone: Smartphone | None):
        self.smartphone = smartphone

    def calculate_storage_used_mb(self) -> float:
        raise NotImplementedError

    def calculate_storage_used(self) -> float:
        return self.calculate_storage_used_mb() / 1024

    def render(self) -> None:
        raise NotImplementedError


class AppGui(Toplevel):
    def __init__(self):
        super().__init__()

    def create_widgets(self) -> None:
        raise NotImplementedError

    def _refresh(self) -> None:
        raise NotImplementedError


class PhotosApp(App):
    APP_NAME = "Photos"

    def __init__(self, phone: Smartphone | None = None) -> None:
        super().__init__(phone)
        self.num_photos: int = 0

    def __str__(self) -> str:
        storage_used = self.calculate_storage_used()
        return f"Photos App - Photos: {self.num_photos}, Storage Used: {storage_used:.2f}GB"

    def storage_cost(self) -> float:
        return 24

    def take_photo(self):
        self.num_photos += 1

    def delete_photo(self):
        if self.num_photos == 0:
            raise ValueError("No photos to delete")
        self.num_photos -= 1

    def calculate_storage_used_mb(self) -> float:
        return self.num_photos * self.storage_cost()

    def render(self) -> None:
        gui = PhotosAppGui(self)
        gui.create_widgets()


class PhotosAppGui(AppGui):
    def __init__(self, backend: PhotosApp):
        super().__init__()
        self.backend = backend

        self.num_photos_var = IntVar()
        self.photos_storage_used_var = StringVar()
        self.photos_error_var = StringVar()

    def create_widgets(self):
        Label(self, text="Photos App").pack()

        photos_frame = Frame(self)
        photos_frame.pack()

        Label(photos_frame, text="Number of Photos:").grid(row=0, column=0)
        Label(photos_frame, textvariable=self.num_photos_var).grid(row=0, column=1)

        Label(photos_frame, text="Storage Used:").grid(row=1, column=0)
        Label(photos_frame, textvariable=self.photos_storage_used_var).grid(
            row=1, column=1
        )

        photos_button_frame = Frame(self)
        photos_button_frame.pack()

        self.take_photo_btn = Button(
            photos_button_frame, text="Take Photos", command=self.take_photo
        )
        self.take_photo_btn.grid(row=0, column=0, padx=5)

        self.delete_photo_btn = Button(
            photos_button_frame, text="Delete Photo", command=self.delete_photo
        )
        self.delete_photo_btn.grid(row=0, column=1, padx=5)

        Label(photos_button_frame, textvariable=self.photos_error_var, fg="red").grid(
            row=1, column=0, columnspan=2
        )

    def _refresh(self) -> None:
        photos_storage_used = self.backend.calculate_storage_used()

        self.num_photos_var.set(self.backend.num_photos)
        self.photos_storage_used_var.set(f"{photos_storage_used:.2f}GB")

        self.photos_error_var.set("")

    def take_photo(self):
        try:
            self.backend.take_photo()
        except MemoryError:
            self.photos_error_var.set("Error: Storage Full")
            return
        except RuntimeError:
            self.photos_error_var.set("Error: Battery Dead")
            return

        self._refresh()

    def delete_photo(self):
        try:
            self.backend.delete_photo()
        except ValueError:
            self.photos_error_var.set("Error: No photos to delete")
        except RuntimeError:
            self.photos_error_var.set("Error: Battery Dead")

        self._refresh()


class YourTubeApp(App):
    APP_NAME = "YourTube"

    def __init__(self, phone: Smartphone | None = None) -> None:
        super().__init__(phone)

        # List of video durations in seconds
        self.videos: list[int] = []

    def __str__(self) -> str:
        storage_used = self.calculate_storage_used()
        num_videos = len(self.videos)

        return (
            f"YourTube App - Videos: {num_videos}, Storage Used: {storage_used:.2f}GB"
        )

    def storage_cost(self, duration: float = 0) -> float:
        return duration * 2

    def save_video(self, video_duration: int):
        """something"""
        self.videos.append(video_duration)

    def delete_video(self, videos_index: int):
        self.videos.pop(videos_index)

    def calculate_storage_used_mb(self) -> float:
        storage_per_second_megabytes = 2
        return sum(duration * storage_per_second_megabytes for duration in self.videos)


class YourTubeAppGui(AppGui):
    def __init__(self, backend: YourTubeApp):
        super().__init__()
        self.backend = backend

        self.num_videos_var = IntVar()
        self.videos_storage_used_var = StringVar()
        self.videos_error_var = StringVar()
        self.duration_var = StringVar(value="0")

    def create_widgets(self) -> None:
        Label(self, text="YourTube App").pack()

        yourtube_frame = Frame(self)
        yourtube_frame.pack()

        Label(yourtube_frame, text="Number of Saved Videos:").grid(row=0, column=0)
        Label(yourtube_frame, textvariable=self.num_videos_var).grid(row=0, column=1)

        Label(yourtube_frame, text="Storage Used:").grid(row=1, column=0)
        Label(yourtube_frame, textvariable=self.videos_storage_used_var).grid(
            row=1, column=1
        )

        button_frame = Frame(self)
        button_frame.pack()

        self.save_video_btn = Button(
            button_frame, text="Save Video", command=self.open_save_video_window
        )
        self.save_video_btn.grid(row=0, column=0, padx=5)

        self.delete_video_btn = Button(
            button_frame, text="Delete Video", command=self.open_delete_video_window
        )
        self.delete_video_btn.grid(
            row=0,
            column=1,
            padx=5,
        )

        Label(button_frame, textvariable=self.videos_error_var, fg="red").grid(
            row=1, column=0, columnspan=2
        )

    def _refresh(self) -> None:
        self.num_videos_var.set(len(self.backend.videos))

        videos_storage_used = self.backend.calculate_storage_used()
        self.videos_storage_used_var.set(f"{videos_storage_used:.2f}GB")

        self.videos_error_var.set("")

    def save_video(self, win: Toplevel):
        try:
            dur = int(self.duration_var.get())
            if dur <= 0:
                raise ValueError("Duration must be positive")
            self.smartphone.save_video(dur)
            win.destroy()
            self._refresh()
        except MemoryError:
            self.videos_error_var.set("Error: Storage Full")
        except RuntimeError:
            self.videos_error_var.set("Error: Battery Dead")
        except ValueError:
            self.videos_error_var.set("Error: Enter a positive integer.")

    def open_save_video_window(self):
        self.videos_error_var.set("")

        win = Toplevel(self.win)
        win.title("Save Video")
        win.geometry("300x150")
        win.grab_set()

        Label(win, text="Video duration (seconds):").pack()
        Entry(win, textvariable=self.duration_var, width=14).pack()

        Button(
            win,
            text="Save",
            command=lambda: self.save_video(win),
        ).pack()

        Label(win, textvariable=self.videos_error_var, fg="red").pack()

    def delete_videos(self, win: Toplevel, button_vars: list[IntVar]):
        if all(var.get() == 0 for var in button_vars):
            self.videos_error_var.set("Error: Please select a video")
            return

        for index in reversed(range(len(button_vars))):
            var = button_vars[index]
            if not var.get():
                continue

            try:
                self.smartphone.delete_video(index)
            except RuntimeError:
                self.videos_error_var.set("Error: Battery Dead")

        win.destroy()
        self._refresh()

    def open_delete_video_window(self):
        self.videos_error_var.set("")

        videos = self.smartphone.yourtube_app.videos
        if not videos:
            self.videos_error_var.set("Error: There are no videos to delete")
            return

        win = Toplevel(self.win)
        win.title("Delete Video")
        win.geometry("320x240")
        win.grab_set()

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


def test_smartphone():
    smartphone = Smartphone(512)
    smartphone.use_battery(30)
    print(smartphone)
    smartphone.battery_saver_mode = True
    smartphone.charge_battery()
    print(smartphone)


def test_photos_app():
    photos_app = PhotosApp()
    for _ in range(5):
        photos_app.take_photo()
    print(photos_app)
    photos_app.delete_photo()
    photos_app.delete_photo()
    print(photos_app)


def test_yourtube_app():
    yourtube_app = YourTubeApp()

    print(yourtube_app)

    yourtube_app.save_video(300)
    yourtube_app.save_video(600)
    yourtube_app.save_video(120)
    print(yourtube_app)

    yourtube_app.delete_video(1)

    print(yourtube_app)
