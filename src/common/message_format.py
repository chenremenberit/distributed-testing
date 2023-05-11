from enum import Enum


class MessageFormatEnum(Enum):
    '''
    控制器相关常量
    节点发送给服务器的信息格式为："header:{device_id}\r\ncommand: {command}\r\nprotocol: {protocol}\r\nreceiver: {receiver_device_id}"
    服务器发送给节点的消息格式为："command: {command}\r\nprotocol: {protocol}\r\nreceiver: {receiver_device_id}"
    '''
    # 服务器处理节点发送的消息需要将其分割为一个字符串list进行校验并对每个元素进行读取处理，对应元素在列表中的位置
    RECEIVING_HEADER_POSITION = 0
    RECEIVING_COMMAND_POSITION = 1
    RECEIVING_PROTOCOL_POSITION = 2
    RECEIVING_RECEIVER_POSITION = 3
