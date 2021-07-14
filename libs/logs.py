# Standard library imports
import logging

# logger setup
logger = logging.getLogger('restore_norm')
# TODO: Нужно будет сделать динамическую инициализацию уровнем логирования - пока работа не стабильна всегда debug
logger.setLevel(logging.DEBUG)

# create file logging  handler
fh = logging.FileHandler(f"logs/verification.log")
# create  stream logging handler
sh = logging.StreamHandler()

# formatter setup
formatter = logging.Formatter('%(asctime)s : %(levelname)s\t: %(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)

# add handlers to logger object
logger.addHandler(fh)
logger.addHandler(sh)
