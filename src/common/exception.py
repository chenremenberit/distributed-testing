
class CommonError(Exception):
    '''
    普通报错
    '''
    def __init__(self, error_msg, error_no=""):
        super(CommonError, self).__init__(error_msg, error_no)
        self.error_msg = error_msg
        self.error_no = error_no

    def __str__(self):
        return str(self.error_msg)


class ConfigError(Exception):
    '''
    配置类问题
    '''
    def __init__(self, error_msg, error_no=""):
        super(ConfigError, self).__init__(error_msg, error_no)
        self.error_msg = error_msg
        self.error_no = error_no

    def __str__(self):
        return str(self.error_msg)


class DeviceCommandError(Exception):
    '''
    执行设备命令报错
    '''
    def __init__(self, error_msg, error_no=""):
        super(DeviceCommandError, self).__init__(error_msg, error_no)
        self.error_msg = error_msg
        self.error_no = error_no

    def __str__(self):
        return str(self.error_msg)
