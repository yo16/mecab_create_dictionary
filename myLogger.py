# coding: utf-8

# logger
# 2017 (c) y.ikeda

from logging import getLogger, StreamHandler, Formatter, DEBUG

def setLogSettings(level):
    # 初期化
    global __myLogger
    __myLogger = getLogger(__name__)

    sh = StreamHandler()    # コンソール出力用のハンドル
    sh.setLevel(level)
    sh.setFormatter(
        Formatter(
            '%(asctime)s.%(msecs)d|%(levelname)s| %(message)s',
            '%Y/%m/%d %H:%M:%S'
        )
    )
    __myLogger.addHandler(sh)
    __myLogger.setLevel(level)

    return 0

def debug(str, logger=None):
    logger = logger or __myLogger
    logger.debug(str)
    return 0

def info(str, logger=None):
    logger = logger or __myLogger
    logger.info(str)
    return 0


setLogSettings(DEBUG)
