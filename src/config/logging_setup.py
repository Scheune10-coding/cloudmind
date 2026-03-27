import logging
import logging.handlers

def setup_logging(level: str, log_file: str):
  root_logger = logging.getLogger()
  root_logger.setLevel(level)

  formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

  stream_handler = logging.StreamHandler()
  stream_handler.setFormatter(formatter)

  file_handler = logging.RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=3)
  file_handler.setFormatter(formatter)

  root_logger.addHandler(stream_handler)
  root_logger.addHandler(file_handler)