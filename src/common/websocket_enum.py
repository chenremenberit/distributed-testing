from enum import Enum


class WebsocketEnum(Enum):
    '''
    Websocket使用的常量
    '''
    WEBSOCKET_HOST = "0.0.0.0"
    WEBSOCKET_PORT = 5678
    WEBSOCKET_TIMEOUT_ENUM = 10