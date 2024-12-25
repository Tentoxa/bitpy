import logging


class LogManager:
    def __init__(self, instance, debug_mode: bool = False):
        self.logger = logging.getLogger(instance.__class__.__name__)
        self.debug_mode = debug_mode
        self._configure_logger()

    def _configure_logger(self):
        if not self.debug_mode:
            return

        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def debug(self, message: str):
        if self.debug_mode:
            self.logger.debug(message)

    def error(self, message: str):
        if self.debug_mode:
            self.logger.error(message)

    def info(self, message: str):
        if self.debug_mode:
            self.logger.info(message)
