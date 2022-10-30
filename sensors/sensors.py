import threading

from utils.network import Network
from random import randint
from service.model.message import Message
from time import sleep
from enum import Enum

TEMPERATURE_SENSOR_DELAY = 1
HEAT_SENSOR_DELAY = 2
WATER_SENSOR_DELAY = 3
HUMIDITY_SENSOR_DELAY = 4
SMOKE_SENSOR_DELAY = 5

TEMPERATURE_SENSOR_PREFIX = "TEMP-"
HEAT_SENSOR_PREFIX = "HEA-"
WATER_SENSOR_PREFIX = "WTR-"
HUMIDITY_SENSOR_PREFIX = "HUM-"
SMOKE_SENSOR_PREFIX = "SMK-"

MIN_VALUE = -100
MAX_VALUE = 100


class SensorType(Enum):
    TEMPERATURE = "temperature"
    HEAT = "heat"
    WATER = "water"
    HUMIDITY = "humidity"
    SMOKE = "smoke"


class BaseSensor(threading.Thread):
    def __init__(self, name: str, delay: int, network: Network):
        super().__init__()
        self.name = name
        self._delay = delay
        self._network = network
        self._value = 0
        self.is_running = False

    def read_value(self) -> None:
        reading = randint(MIN_VALUE, MAX_VALUE)
        self._value = reading

    def publish(self, message: Message) -> None:
        self._network.publish(message)

    def run(self):
        self.is_running = True
        try:
            while self.is_running:
                self.read_value()
                message = Message(sensor_name=self.name, value=self._value)
                print(f"Publishing message: {message}")
                self.publish(message)
                sleep(self._delay)
            print(f"Stopping sensor {self.name}...")
        finally:
            print(f"Stopped sensor: {self.name}")


class TemperatureSensor(BaseSensor):
    def __init__(self, name: str, network: Network):
        super().__init__(
            TEMPERATURE_SENSOR_PREFIX + name, TEMPERATURE_SENSOR_DELAY, network
        )


class HeatSensor(BaseSensor):
    def __init__(self, name: str, network: Network):
        super().__init__(HEAT_SENSOR_PREFIX + name, HEAT_SENSOR_DELAY, network)


class WaterSensor(BaseSensor):
    def __init__(self, name: str, network: Network):
        super().__init__(WATER_SENSOR_PREFIX + name, WATER_SENSOR_DELAY, network)


class HumiditySensor(BaseSensor):
    def __init__(self, name: str, network: Network):
        super().__init__(HUMIDITY_SENSOR_PREFIX + name, HUMIDITY_SENSOR_DELAY, network)


class SmokeSensor(BaseSensor):
    def __init__(self, name: str, network: Network):
        super().__init__(SMOKE_SENSOR_PREFIX + name, SMOKE_SENSOR_DELAY, network)
