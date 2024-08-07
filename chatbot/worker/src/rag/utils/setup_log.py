import logging
import pathlib


def setup_logger(module_name):
    ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    file_handler = logging.FileHandler(ROOT_DIR / "logs" / "rag_chatbot.log")

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
