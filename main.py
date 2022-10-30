import threading

from sensors.sensor_factory import BuildingSensorFactory, NatureSensorFactory
from sensors.sensors import SensorType


if __name__ == '__main__':
    sensors = []
    building_sensor_factory = BuildingSensorFactory()
    nature_sensor_factory = NatureSensorFactory()
    sensors.append(building_sensor_factory.create("sensor_1", SensorType.SMOKE))
    sensors.append(building_sensor_factory.create("sensor_2", SensorType.HEAT))
    sensors.append(building_sensor_factory.create("sensor_3", SensorType.TEMPERATURE))
    sensors.append(nature_sensor_factory.create("sensor_4", SensorType.WATER))
    sensors.append(nature_sensor_factory.create("sensor_5", SensorType.HUMIDITY))
    threads = []
    for sensor in sensors:
        thread = threading.Thread(target=sensor.run)
        threads.append(thread)
        thread.start()
    try:
        while True:
            pass
    except KeyboardInterrupt as e:
        for sensor in sensors:
            sensor.is_running = False
        while threads:
            for thread in threads:
                thread.join(0.2)
                if thread.is_alive():
                    print("Thread not ready to join...")
                else:
                    print("Thread successfully joined")
                    threads.remove(thread)
        print("Program stopped")
