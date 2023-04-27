import time
import os

from common.exception import CommonError


class Logger(object):
    def __init__(self, name):
        '''
        通用日志记录类，logging模块在多线程下会出现多次打印日志的问题，故简单写个日志记录类
        :param name:
        '''
        if not name:
            raise CommonError("Please Input Logger Name!")
        self.name = name

    def info(self, *args, **kwargs):
        self.record_log('info', args, kwargs)

    def warning(self, *args, **kwargs):
        self.record_log('warning', args, kwargs)

    def error(self, *args, **kwargs):
        self.record_log('error', args, kwargs)

    def debug(self, *args, **kwargs):
        self.record_log('debug', args, kwargs)

    def record_log(self, level, *args, **kwargs):
        msg = ""
        for value in args:
            if len(value) > 0 :
                if isinstance(value, list):
                    msg = msg + ",".join(value)
                else:
                    for context in value:
                        msg = msg + " " + str(context)
        if kwargs:
            msg = msg + str(kwargs)
        self.write_log(level, msg)

    def write_log(self, log_level, msg):
        '''
        根据配置的输出格式来打印日志
        '''
        time_now = time.strftime('%Y-%m-%d %H:%M:%S')
        log_prefix = time_now + " " + self.name
        msg = log_prefix + " " + log_level + " " + msg
        self.record_msg_to_console(msg)

    @staticmethod
    def record_msg_to_console(msg):
        '''
        只在控制台打印日志
        '''
        print(msg)

    def record_msg_to_file(self, msg):
        '''
        记录日志到文件
        '''
        log_file_path = self._find_log_path() + "/log/app-" + time.strftime("%m%d") + ".log"
        with open(log_file_path, "a", encoding="utf-8") as logfile:
            logfile.write(msg + "\n")
            logfile.flush()

    def _find_log_path(self):
        cur_dir = os.getcwd()
        while True:
            if cur_dir == "/" or cur_dir.endswith(":\\"):
                break
            log_path = os.path.join(cur_dir, 'log')
            if os.path.exists(log_path):
                return cur_dir
            cur_dir = os.path.dirname(cur_dir)
        raise CommonError("Please call inside source root directory")