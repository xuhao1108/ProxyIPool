import sys
import logging

from setting import LOG_LEVEL, LOG_TIME, LOG_FILENAME, LOG_FORMAT


class Log(object):
    """
    日志记录
    """
    def __init__(self):
        """
        初始化logger
        """
        # 1. 获取一个logger对象
        self._logger = logging.getLogger()
        # 2. 设置format对象
        self.formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_TIME)
        # 3.1 设置文件日志模式
        self._logger.addHandler(self._get_file_handler())
        # 3.2 设置终端日志模式
        self._logger.addHandler(self._get_console_handler())
        # 4. 设置日志等级
        self._logger.setLevel(LOG_LEVEL)

    def _get_file_handler(self):
        """
        获取文件handler对象
        :return:
        """
        # 1. 获取一个文件日志handler
        file_handler = logging.FileHandler(filename=LOG_FILENAME, encoding='utf-8')
        # 2. 设置日志格式
        file_handler.setFormatter(self.formatter)
        # 3. 返回handler对象
        return file_handler

    def _get_console_handler(self):
        """
        获取控制台handler对象
        :return:
        """
        # 1. 获取一个文件日志handler
        console_handler = logging.StreamHandler(sys.stdout)
        # 2. 设置日志格式
        console_handler.setFormatter(self.formatter)
        # 3. 返回handler对象
        return console_handler

    @property
    def get_logger(self):
        """
        单例模式，获取单例对象
        :return:
        """
        return self._logger


# 创建单例对象
logger = Log().get_logger
