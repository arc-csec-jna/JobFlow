import logging

def log_setup():
    logging.basicConfig(
        level=logging.INFO,
        format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )