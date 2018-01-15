# -*- coding: utf-8 -*-
__author__ = 'vincent'

import sys
import time
import logging
import uuid
import flask

# 颜色设置
COLOR_RED    = '\033[1;31m'
COLOR_GREEN  = '\033[1;32m'
COLOR_YELLOW = '\033[1;33m'
COLOR_BLUE   = '\033[1;34m'
COLOR_PURPLE = '\033[1;35m'
COLOR_CYAN   = '\033[1;36m'
COLOR_GRAY   = '\033[1;37m'
COLOR_WHITE  = '\033[1;38m'
COLOR_RESET  = '\033[1;0m'

# 设置日志级别颜色
LOG_COLORS = {
    'DEBUG'  : COLOR_BLUE,
    'INFO'   : COLOR_GREEN,
    'WARNING': COLOR_YELLOW,
    'ERROR'  : COLOR_RED
}





def request_id():
    # 如果当前存在 request_id 则返回当前的 request_id， 否则新生成一个 request_id
    # 优先顺序
    # 如果我们已经创建了 request_id，并已将其存入了 请求上下文 g 中， 则优先使用它
    # 否则 重新生成一个 request_id，并将其存入了 请求上下文 g 中， 然后使用 这个新生成的 request_id
    if getattr(flask.g, 'request_id', None):
        return flask.g.request_id

    new_uuid = uuid.uuid4()
    flask.g.request_id = new_uuid

    return new_uuid

class RequestIdFilter(logging.Filter):
    # 这是一个日志过滤器，它将获取一个 唯一请求ID，
    # 注意，如果存在上下文，则直接从上下文中获取请求ID，或者生成请求ID。
    def filter(self, record):
        # 判断当前上下文是否存在，如果存在，则通过 request_id() 获取 request_id； 否则可能是系统及的错误，则返回空值
        record.request_id = request_id() if flask.has_request_context() else ''
        return True



class ColoredFormatter(logging.Formatter):
    def format(self, record):
        color_cap = LOG_COLORS[record.levelname]
        log_time = time.localtime(record.created)
        log_time = time.strftime('%Y/%m/%d %H:%M:%S', log_time)

        log_line = '{}{} [{}][{}] [RequestID:{}]\033[0m {}'.format(
            color_cap,
            log_time,
            record.levelname,
            record.name,
            record.request_id,
            record.msg)

        return log_line


def get_logger(logger_name=None):
    '''
    获取日志对象
    '''
    if not logger_name:
        logger_name = 'SYSTEM'

    logger = logging.getLogger(logger_name)
    if log_hander not in logger.handlers:
        logger.addHandler(log_hander)
        logger.setLevel(logging.DEBUG)

    return logger


# 设置日志流数据流向终端
log_hander = logging.StreamHandler(stream=sys.stdout)
# 设置日志数据流向指定文件
# log_hander = logging.FileHandler('/Users/vincent/MyGitWarehouse/it-cloud-lab/api_service/logs/app.log')
# 设置日志级别
log_hander.setLevel(logging.DEBUG)
# 在日志中添加 唯一请求ID
log_hander.addFilter(RequestIdFilter())
# 设置日志格式信息
log_hander.setFormatter(ColoredFormatter())
