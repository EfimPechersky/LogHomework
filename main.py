from fastapi import FastAPI
import datetime
import hashlib
import socket
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
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

logger = get_logger("fastapiapp_logger")
logger.info("Start FastApi App")
app = FastAPI()

@app.get("/auth")
async def root():
    logger.debug("Someone connected")
    time_str=str(datetime.datetime.now())
    id=hashlib.md5(time_str.encode()).hexdigest()
    logger.info("Id created")
    return {"id": id}
