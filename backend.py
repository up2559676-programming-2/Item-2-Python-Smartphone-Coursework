class Smartphone:
    def __init__(self, storage_capacity: int) -> None:
        self.storage_capacity = storage_capacity
        self.battery: int = 100
        self.battery_saver_mode: bool = False

    def __str__(self) -> str:
        battery_saver_mode = "Enabled" if self.battery_saver_mode else "Disabled"
        return f"BnL Smartphone - Storage: {self.storage_capacity}GB, Battery: {self.battery}%, Battery Saver Mode: {battery_saver_mode}"

    def use_battery(self, amount: int):
        self.battery = max(0, self.battery - amount)

    def charge_battery(self):
        if self.battery_saver_mode:
            self.battery = max(80, self.battery)
        else:
            self.battery = 100


def test_smartphone():
    smartphone = Smartphone(512)
    smartphone.use_battery(30)
    print(smartphone)
    smartphone.battery_saver_mode = True
    smartphone.charge_battery()
    print(smartphone)


test_smartphone()
