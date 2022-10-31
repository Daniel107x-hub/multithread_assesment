import queue
import sys
import logging

from sensors.sensor_factory import BuildingSensorFactory, NatureSensorFactory
from sensors.sensors import SensorType
from utils.network import Network
from service.database_service import DatabaseService
from service.repository.repository import Repository
from logger.logger import Logger

logging.basicConfig(level=logging.INFO)


def stop_sensors(sensors_list: list):
    for sensor in sensors_list:
        sensor.is_running = False
    while sensors_list:
        for sensor in sensors_list:
            sensor.join(0.2)
            if sensor.is_alive():
                logging.debug("Sensor not ready to join...")
            else:
                logging.debug("Sensor successfully joined.")
                sensors_list.remove(sensor)
    logging.info("Successfully stopped all sensors")


def stop_loggers(loggers_list: list):
    while loggers_list:
        for logger in loggers_list:
            logger.join(0.2)
            if logger.is_alive():
                logging.debug("Logger not ready to join...")
            else:
                logging.debug("Logger successfully joined.")
                loggers_list.remove(logger)
    logging.info("Successfully stopped all loggers")


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
    consumers = [Logger(repository, network, i) for i in range(0, 5)]

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
        logging.info("Finishing program execution...")
        stop_sensors(sensors)
        network.publish(None)
        stop_loggers(consumers)
        logging.info("Program finished.")
        sys.exit(e)
