# -*- coding: UTF-8 -*-
import logging
import os
import sys
import time
import ConfigParser
import trace
import datetime

from logging.handlers import TimedRotatingFileHandler

MyLogLevel = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR,
              "CRITICAL": logging.CRITICAL}

CONFIG_LEVEL = "level"


def CreatLogger(loggername, filename=None, config_filename=None, config_sectionname=None, levelinfo="INFO"):
    """
    :param loggername: 日志名称
    :param filename: 日志的保存文件，假如为None，则不保存为文件
    :param config_filename: 配置文件的名称，假如为None，则根据level生成屏幕打印
    :param config_sectionname: 配置文件中的设置日志的字段，同上
    :param level: 假如不通过配置文件设置日志，则根据该值设置日志级别
    :return: None
    """
    logger = logging.getLogger(loggername)

    if config_filename and config_sectionname:
        cf = ConfigParser.ConfigParser()
        cf.read(config_filename)
        level = cf.get(config_sectionname, CONFIG_LEVEL)
        logger.setLevel(MyLogLevel[level])
    else:
        logger.setLevel(MyLogLevel[levelinfo])

    formatter = logging.Formatter('[%(asctime)s] %(filename)s [line:%(lineno)d] %(levelname)s-%(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(MyLogLevel[levelinfo])
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if filename:
        fh = TimedRotatingFileHandler(filename, when="midnight")
        fh.suffix = "%Y-%m-%d.log"
        fh.setFormatter(formatter)
        logger.addHandler(fh)


def LoggerExcept(logger):
    if not logger:
        return
    info = sys.exc_info()
    for file, lineno, function, text in traceback.extract_tb(info[2]):
        logger.error('%s line:%s in %s'%(file,str(lineno), function))
        logger.error('%s'%(text))
    logger.error("** %s: %s"%info[:2])

if __name__ == '__main__':
    TEST_CONFIG = './test.ini'
    TEST_LOGGERFILE = './test.log'
    TEST_SECTION_NAME = 'test_log'
    CreatLogger('test_mylog',TEST_LOGGERFILE,TEST_CONFIG,TEST_SECTION_NAME)
    test_logger = logging.getLogger('test_mylog')
    while 1:
        test_logger.info('this message is to test the logger')
        time.sleep(1)

