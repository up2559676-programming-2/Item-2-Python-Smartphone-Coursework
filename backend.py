from tkinter import (
    IntVar,
    StringVar,
    Toplevel,
    Label,
    Button,
    Frame,
    Entry,
    Checkbutton,
)


class StorageFullError(Exception):
    def __init__(self, used: float, capacity: int, message: str | None = None):
        self.used = used
        self.capacity = capacity
        self.message = message or f"Storage full: {used:.2f}/{capacity} bytes used"
        super().__init__(self.message)


class BatteryEmptyError(Exception):
    def __init__(self, level: int, required: int = 1, message: str | None = None):
        self.level = level
        self.required = required
        self.message = (
            message or f"Battery empty: {level}% remaining (requires ≥ {required}%)"
        )
        super().__init__(self.message)


class Smartphone:
    def __init__(self, storage_capacity: int) -> None:
        if storage_capacity <= 0:
            storage_capacity = 256

        self.storage_capacity = storage_capacity
        self.battery: int = 100
        self.battery_saver_mode: bool = False
        self.apps: tuple[AppGui, ...] = (
            PhotosAppGui(PhotosApp()),
            YourTubeAppGui(YourTubeApp()),
        )

    def __str__(self) -> str:
        return f"BnL Smartphone - Storage: {self.storage_capacity}GB, Battery: {self.battery}%, Battery Saver Mode: {self.battery_saver_str}"

    @property
    def _storage_capacity_mb(self) -> int:
        return self.storage_capacity * 1024

    @property
    def battery_saver_str(self) -> str:
        return "Enabled" if self.battery_saver_mode else "Disabled"

    @property
    def storage_left_mb(self) -> float:
        return self._storage_capacity_mb - self.total_storage_used_mb()

    @property
    def storage_left(self) -> float:
        return self.storage_left_mb / 1024

    def use_battery(self, amount: int):
        self.battery = max(0, self.battery - amount)

    def charge_battery(self):
        if self.battery_saver_mode:
            self.battery = max(80, self.battery)
        else:
            self.battery = 100

    def consume_battery(self):
        if self.battery < 2:
            raise BatteryEmptyError(self.battery, 2)

        self.use_battery(2)

    def total_storage_used_mb(self) -> float:
        return sum(app.backend.calculate_storage_used_mb() for app in self.apps)


class App:
    def calculate_storage_used_mb(self) -> float:
        raise NotImplementedError

    def calculate_storage_used(self) -> float:
        return self.calculate_storage_used_mb() / 1024


class PhotosApp(App):
    APP_NAME = "Photos"

    def __init__(self) -> None:
        self.num_photos: int = 0

    def __str__(self) -> str:
        storage_used = self.calculate_storage_used()
        return f"Photos App - Photos: {self.num_photos}, Storage Used: {storage_used:.2f}GB"

    def storage_cost(self) -> float:
        return 24

    def take_photo(self, phone: Smartphone | None = None):
        if phone is not None:
            phone.consume_battery()

            if phone.storage_left_mb < self.storage_cost():
                raise StorageFullError(phone.storage_left, phone.storage_capacity)
        self.num_photos += 1

    def delete_photo(self, phone: Smartphone | None = None):
        if phone is not None:
            phone.consume_battery()

        if self.num_photos == 0:
            raise ValueError("No photos to delete")
        self.num_photos -= 1

    def calculate_storage_used_mb(self) -> float:
        return self.num_photos * self.storage_cost()


class YourTubeApp(App):
    APP_NAME = "YourTube"

    def __init__(self) -> None:
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

    def save_video(self, video_duration: int, phone: Smartphone | None = None):
        if phone is not None:
            phone.consume_battery()

        if video_duration <= 0:
            raise ValueError("Duration must be positive")

        if phone is not None and phone.storage_left_mb < self.storage_cost(
            video_duration
        ):
            raise StorageFullError(phone.storage_left, phone.storage_capacity)
        self.videos.append(video_duration)

    def delete_video(self, videos_index: int, phone: Smartphone | None = None):
        if phone is not None:
            phone.consume_battery()

        self.videos.pop(videos_index)

    def calculate_storage_used_mb(self) -> float:
        storage_per_second_megabytes = 2
        return sum(duration * storage_per_second_megabytes for duration in self.videos)


class AppGui:
    APP_NAME = "Unnamed App"

    def __init__(self, backend: App) -> None:
        self.backend = backend
        self.phone: Smartphone | None = None

    def init_vars(self) -> None:
        raise NotImplementedError

    def create_widgets(self, win: Toplevel) -> None:
        raise NotImplementedError

    def _refresh(self) -> None:
        raise NotImplementedError

    def render(self, phone: Smartphone) -> Toplevel:
        self.phone = phone

        win = Toplevel()
        win.grab_set()
        self.init_vars()
        self.create_widgets(win)
        return win


class PhotosAppGui(AppGui):
    APP_NAME = "Photos"

    def __init__(self, backend: PhotosApp):
        super().__init__(backend)

    def init_vars(self):
        self.num_photos_var = IntVar()
        self.photos_storage_used_var = StringVar()
        self.photos_error_var = StringVar()
        self._refresh()

    def create_widgets(self, win: Toplevel):
        Label(win, text="Photos App").pack()

        photos_frame = Frame(win)
        photos_frame.pack()

        Label(photos_frame, text="Number of Photos:").grid(row=0, column=0)
        Label(photos_frame, textvariable=self.num_photos_var).grid(row=0, column=1)

        Label(photos_frame, text="Storage Used:").grid(row=1, column=0)
        Label(photos_frame, textvariable=self.photos_storage_used_var).grid(
            row=1, column=1
        )

        photos_button_frame = Frame(win)
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
        assert isinstance(self.backend, PhotosApp)

        photos_storage_used = self.backend.calculate_storage_used()

        self.num_photos_var.set(self.backend.num_photos)
        self.photos_storage_used_var.set(f"{photos_storage_used:.2f}GB")

        self.photos_error_var.set("")

    def take_photo(self):
        assert isinstance(self.backend, PhotosApp)
        assert self.phone is not None

        try:
            self.backend.take_photo(self.phone)
        except StorageFullError as e:
            self.photos_error_var.set(e.message)
            return
        except BatteryEmptyError as e:
            self.photos_error_var.set(e.message)
            return

        self._refresh()

    def delete_photo(self):
        assert isinstance(self.backend, PhotosApp)
        assert self.phone is not None

        try:
            self.backend.delete_photo(self.phone)
        except BatteryEmptyError as e:
            self.photos_error_var.set(e.message)
            return
        except ValueError:
            self.photos_error_var.set("No photos to delete")
            return

        self._refresh()


class YourTubeAppGui(AppGui):
    APP_NAME = "YourTube"

    def __init__(self, backend: YourTubeApp):
        super().__init__(backend)

        self.action_frame: Frame | None = None
        self.delete_videos_frame: Frame | None = None

    def init_vars(self):
        self.num_videos_var = IntVar()
        self.videos_storage_used_var = StringVar()
        self.videos_error_var = StringVar()
        self.duration_var = StringVar(value="Write the duration here")
        self._refresh()

    def create_widgets(self, win: Toplevel) -> None:
        assert isinstance(self.backend, YourTubeApp)

        win.geometry("350x300")
        win.title("YourTube App")

        Label(win, text="YourTube App").pack()

        yourtube_frame = Frame(win)
        yourtube_frame.pack()

        Label(yourtube_frame, text="Number of Saved Videos:").grid(row=0, column=0)
        Label(yourtube_frame, textvariable=self.num_videos_var).grid(row=0, column=1)

        Label(yourtube_frame, text="Storage Used:").grid(row=1, column=0)
        Label(yourtube_frame, textvariable=self.videos_storage_used_var).grid(
            row=1, column=1
        )

        self.action_frame = Frame(win)
        self.action_frame.pack()

        self._create_save_video_frame(self.action_frame).grid(column=0, row=1)

        self.delete_videos_frame = self._create_delete_videos_frame(self.action_frame)
        self.delete_videos_frame.grid(column=0, row=2)

        Label(self.action_frame, textvariable=self.videos_error_var, fg="red").grid(
            column=0, row=3
        )

    def _refresh(self) -> None:
        assert isinstance(self.backend, YourTubeApp)

        self.num_videos_var.set(len(self.backend.videos))

        videos_storage_used = self.backend.calculate_storage_used()
        self.videos_storage_used_var.set(f"{videos_storage_used:.2f}GB")

        self.videos_error_var.set("")

        if self.delete_videos_frame is not None:
            self.delete_videos_frame.destroy()

        if self.action_frame is not None:
            self.delete_videos_frame = self._create_delete_videos_frame(
                self.action_frame
            )
            self.delete_videos_frame.grid(column=0, row=2)

    def _create_save_video_frame(self, parent: Frame) -> Frame:
        save_video_frame = Frame(parent)

        Entry(save_video_frame, textvariable=self.duration_var, width=25).pack(
            side="left"
        )
        Button(
            save_video_frame,
            text="Save",
            command=lambda: self.save_video(),
        ).pack(side="right")

        return save_video_frame

    def save_video(self):
        assert isinstance(self.backend, YourTubeApp)
        assert self.phone is not None

        try:
            dur = int(self.duration_var.get())
            self.backend.save_video(dur, self.phone)
        except StorageFullError as e:
            self.videos_error_var.set(e.message)
            return
        except BatteryEmptyError as e:
            self.videos_error_var.set(e.message)
            return
        except ValueError:
            self.videos_error_var.set("Error: Enter a positive integer.")
            return

        self._refresh()

    def _create_delete_videos_frame(self, parent: Frame) -> Frame:
        assert isinstance(self.backend, YourTubeApp)

        delete_video_frame = Frame(parent)
        Label(delete_video_frame, text="Select videos to delete:").pack()

        button_vars: list[IntVar] = []
        for i, dur in enumerate(self.backend.videos):
            size_mb = dur * 2

            var = IntVar()
            Checkbutton(
                delete_video_frame,
                text=f"Video {i + 1}:  {dur}s  ({size_mb} MB)",
                variable=var,
            ).pack()
            button_vars.append(var)

        Button(
            delete_video_frame,
            text="Delete Selected",
            command=lambda: self.delete_videos(button_vars),
        ).pack()

        return delete_video_frame

    def delete_videos(self, button_vars: list[IntVar]):
        assert isinstance(self.backend, YourTubeApp)

        if all(var.get() == 0 for var in button_vars):
            self.videos_error_var.set("Error: Please select a video")
            return

        for index in reversed(range(len(button_vars))):
            var = button_vars[index]
            if not var.get():
                continue

            try:
                self.backend.delete_video(index)
            except BatteryEmptyError as e:
                self.videos_error_var.set(e.message)

        self._refresh()


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
