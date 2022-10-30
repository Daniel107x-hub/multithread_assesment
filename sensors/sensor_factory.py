from abc import abstractmethod
from .sensors import (
    BaseSensor,
    TemperatureSensor,
    HeatSensor,
    WaterSensor,
    HumiditySensor,
    SmokeSensor,
    SensorType,
)
from utils.network import Network


class SensorFactory:
    def __init__(self, network: Network):
        self._network = network

    @abstractmethod
    def create(self, name: str, sensor_type: SensorType) -> BaseSensor:
        pass


class BuildingSensorFactory(SensorFactory):
    def create(self, name: str, sensor_type: SensorType) -> BaseSensor:
        if sensor_type == SensorType.HEAT:
            return HeatSensor(name, self._network)
        if sensor_type == SensorType.SMOKE:
            return SmokeSensor(name, self._network)
        if sensor_type == SensorType.TEMPERATURE:
            return TemperatureSensor(name, self._network)
        raise Exception(f"Sensor type: {sensor_type} not in BuildingSensorFactory")


class NatureSensorFactory(SensorFactory):
    def create(self, name: str, sensor_type: SensorType) -> BaseSensor:
        if sensor_type == SensorType.WATER:
            return WaterSensor(name, self._network)
        if sensor_type == SensorType.HUMIDITY:
            return HumiditySensor(name, self._network)
        raise Exception(f"Sensor type: {sensor_type} not in NatureSensorFactory")
