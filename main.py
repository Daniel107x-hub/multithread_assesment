import queue
import sys

from sensors.sensor_factory import BuildingSensorFactory, NatureSensorFactory
from sensors.sensors import SensorType
from utils.network import Network
from service.database_service import DatabaseService
from service.repository.repository import Repository
from logger.logger import Logger


if __name__ == "__main__":
    # Set up repository
    db = DatabaseService()
    repository = Repository(db)
    repository.create_tables()

    # Setting up the network
    buffer = queue.Queue()
    network = Network(buffer)

    # Creating sensors
    building_sensor_factory = BuildingSensorFactory(network)
    nature_sensor_factory = NatureSensorFactory(network)
    sensors = [
        building_sensor_factory.create("sensor_1", SensorType.SMOKE),
        building_sensor_factory.create("sensor_2", SensorType.HEAT),
        building_sensor_factory.create("sensor_3", SensorType.TEMPERATURE),
        nature_sensor_factory.create("sensor_4", SensorType.WATER),
        nature_sensor_factory.create("sensor_5", SensorType.HUMIDITY),
    ]

    # Setting up consumers
    consumers = [
        Logger(repository, network, 1),
        Logger(repository, network, 2),
        Logger(repository, network, 3),
        Logger(repository, network, 4),
        Logger(repository, network, 5),
    ]

    # Starting sensors and consumers
    for consumer in consumers:
        consumer.start()

    for sensor in sensors:
        sensor.start()

    # Main loop
    try:
        while True:
            pass
    except KeyboardInterrupt as e:
        # Stop sensors
        for sensor in sensors:
            sensor.is_running = False

        while sensors:
            for sensor in sensors:
                sensor.join(0.2)
                if sensor.is_alive():
                    print("Sensor thread not ready to join...")
                else:
                    print("Sensor thread successfully joined")
                    sensors.remove(sensor)

        # Stop consumers
        network.publish(None)
        while consumers:
            for consumer in consumers:
                consumer.join(0.2)
                if consumer.is_alive():
                    print("Consumer not ready to join...")
                else:
                    print("Consumer successfully joined")
                    consumers.remove(consumer)
        print("Program finished")
        sys.exit(e)
