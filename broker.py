import time
import paho.mqtt.client as mqtt_client
import random
import requests
import socket
import logging
import sys
import hashlib
from logging.handlers import TimedRotatingFileHandler
hashhost=hashlib.md5(socket.gethostname().encode()).hexdigest()
FORMATTER_STRING = "%(asctime)s - "+hashhost+" - %(name)s - %(levelname)s - %(message)s"
FORMATTER = logging.Formatter(FORMATTER_STRING)
LOG_FILE = "/home/efim/my_app.log" # use fancy libs to make proper temp file

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    logger.addHandler(console_handler)

    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    logger.addHandler(file_handler)

    return logger

logger = get_logger("publisher_logger")
logger.info("Start publisher")
try:
    r = requests.get('http://51.250.123.8:8000/auth')
    id = r.json()['id']
    logger.debug("Got ID from fastapi app")
except:
    logger.error("Connection to fastapi app failed")
    exit()


broker="broker.emqx.io"

try:
    client = mqtt_client.Client(id)
    logger.debug("Created client")
except:
    logger.error("Cannot create client")
    exit()

logger.debug("Connecting to broker:"+broker)
try:
    client.connect(broker)
    logger.debug("Connected to broker")
except:
    logger.error("Cannot connect to broker")
    exit()
client.loop_start() 
logger.info("Publishing")
try:
    for i in range(10):
        state="on" if random.randint(0,1) == 0 else "off"
        state=state+'Efim'
        client.publish("lab/leds/state", state)
        logger.info("Published: "+state)
        time.sleep(2)
except:
    logger.error("Script stopped by user")
    
client.disconnect()
logger.debug("Client disconnected")
client.loop_stop()
logger.info("Publisher stopped")