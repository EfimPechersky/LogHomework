import time
import sys
import paho.mqtt.client as mqtt_client
import random
import requests
import socket
import logging
import sys
import hashlib
from logging.handlers import TimedRotatingFileHandler

ipaddr=""

hashhost=hashlib.md5(socket.gethostname().encode()).hexdigest()
FORMATTER_STRING = "%(asctime)s - "+hashhost+" - %(name)s - %(levelname)s - %(message)s"
FORMATTER = logging.Formatter(FORMATTER_STRING)
LOG_FILE = "./my_app.log" # use fancy libs to make proper temp file

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

logger = get_logger("subscriber_logger")
broker="broker.emqx.io"
logger.info("Start subscriber")
def on_message(client, userdata, message):
    time.sleep(1)
    data = str(message.payload.decode("utf-8"))
    logger.info('Received message = "'+data+'"')

try:
    r = requests.get('http://'+ipaddr+':8000/auth')
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
client.on_message=on_message

logger.debug("Connecting to broker:"+broker)

try:
    client.connect(broker)
    logger.debug("Connected to broker")
except:
    logger.error("Cannot connect to broker")
    exit()

client.loop_start() 
logger.info("Subcribing")
client.subscribe("lab/leds/state")
try:
    time.sleep(1800)
except:
    logger.error("User stopped script")
client.disconnect()
logger.debug("Disconnected")
client.loop_stop()
