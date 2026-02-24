class Smartphone:
    def __init__(self, storage_capacity: int) -> None:
        if storage_capacity <= 0:
            raise ValueError("Storage capacity must be positive")

        self.storage_capacity = storage_capacity
        self.battery: int = 100
        self.battery_saver_mode: bool = False

        self.photos_app = PhotosApp()
        self.yourtube_app = YourTubeApp()

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
        return (
            self.photos_app.calculate_storage_used_mb()
            + self.yourtube_app.calculate_storage_used_mb()
        )

    def _check_storage_available(self, additional_storage: float):
        if (
            self.total_storage_used_mb() + additional_storage
            > self._storage_capacity_mb
        ):
            raise MemoryError("Not enough storage available")

    def take_photo(self):
        self._check_storage_available(24)

        self.photos_app.take_photo()
        self._consume_app_usage()

    def delete_photo(self):
        self.photos_app.delete_photo()
        self._consume_app_usage()

    def save_video(self, duration: int):
        self._check_storage_available(duration * 2)

        self.yourtube_app.save_video(duration)
        self._consume_app_usage()

    def delete_video(self, index: int):
        self.yourtube_app.delete_video(index)
        self._consume_app_usage()


class App:
    def calculate_storage_used_mb(self) -> float: ...

    def calculate_storage_used(self) -> float:
        return self.calculate_storage_used_mb() / 1024


class PhotosApp(App):
    def __init__(self) -> None:
        self.num_photos: int = 0

    def __str__(self) -> str:
        storage_used = self.calculate_storage_used()
        return f"Photos App - Photos: {self.num_photos}, Storage Used: {storage_used:.2f}GB"

    def take_photo(self):
        self.num_photos += 1

    def delete_photo(self):
        self.num_photos -= 1

    def calculate_storage_used_mb(self) -> float:
        storage_per_photo_megabytes = 24
        return self.num_photos * storage_per_photo_megabytes


class YourTubeApp(App):
    def __init__(self) -> None:
        # List of video durations in seconds
        self.videos: list[int] = []

    def __str__(self) -> str:
        storage_used = self.calculate_storage_used()
        num_videos = len(self.videos)

        return (
            f"YourTube App - Videos: {num_videos}, Storage Used: {storage_used:.2f}GB"
        )

    def save_video(self, video_duration: int):
        self.videos.append(video_duration)

    def delete_video(self, videos_index: int):
        self.videos.pop(videos_index)

    def calculate_storage_used_mb(self) -> float:
        storage_per_second_megabytes = 2
        return sum(duration * storage_per_second_megabytes for duration in self.videos)


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
