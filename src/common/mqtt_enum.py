from enum import Enum


class MQTTReturnCode(Enum):
    '''
    MQTT返回码
    '''
    # 处理成功
    CONNECTION_SUCCESS = "0"
    # 连接被拒绝，不可接受的协议版本
    CONNECTION_REJECTED_FOR_UNACCEPTABLE_PROTOCOL_VERSION = "1"
    # 连接被拒绝，标识符拒绝
    CONNECTION_REJECTED_FOR_IDENTIFIER = "2"
    # 连接被拒绝，服务器不可用
    CONNECTION_REJECTED_FOR_SERVER_UNAVAILABLE = "3"
    # 连接被拒绝，错误的用户名或密码
    CONNECTION_DENIED_FOR_INCORRECT_USERNAME_OR_PASSWORD = "4"
    # 连接被拒绝，未经授权
    CONNECTION_DENIED_FOR_UNAUTHORIZED = "5"


class MQTTServerEnum(Enum):
    '''
    MQTT服务器各类信息
    '''
    MQTT_SERVER_USERNAME = "kaihong"
    MQTT_SERVER_PASSWORD = "kaihong123"
    MQTT_SERVER_HOST = "71.255.2.21"
    MQTT_SERVER_PORT = 1883


class CommonEnum(Enum):
    '''
    MQTT服务器超时时间
    '''
    MQTT_TIMEOUT_ENUM = 60
