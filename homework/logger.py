import logging

error_logger = logging.getLogger("Error logger")
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler('error_log.txt', 'a', 'utf-8')
error_formatter = logging.Formatter("%(levelname)-8s [%(asctime)s]  %(message)s")
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)

info_logger = logging.getLogger("Info logger")
info_logger.setLevel(logging.INFO)
info_handler = logging.FileHandler('info_log.txt', 'a', 'utf-8')
info_formatter = logging.Formatter("%(levelname)-8s [%(asctime)s]  %(message)s")
info_handler.setFormatter(info_formatter)
info_logger.addHandler(info_handler)