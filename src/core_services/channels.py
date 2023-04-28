from common.mqtt_enum import MQTTServerEnum
from common.websocket_enum import WebsocketEnum
from core_services.modbus_channel import ModBusChannel
from core_services.mqtt_channel import MQTTChannel
from core_services.websocket_channel import WebSocketChannel
from util.logger_manager_ment import Logger


class Channel:
    def __init__(self, device_id):
        '''
        channel类，主机代理
        :return:
        '''
        self.device_id = device_id
        self.protocol_type_dict = {"MQTT": {"class": "MQTTChannel",
                                            "host": MQTTServerEnum.MQTT_SERVER_HOST.value,
                                            "port": MQTTServerEnum.MQTT_SERVER_PORT.value},
                                   "WebSocket": {"class": "WebSocketChannel",
                                                 "host": WebsocketEnum.WEBSOCKET_HOST.value,
                                                 "port": WebsocketEnum.WEBSOCKET_PORT.value},
                                   "Modbus": {"class": "ModBusChannel"}}
        self.channel_function_dict = {"MQTT": {"send_message_func_name": "publish_message_to_mqtt_server",
                                               "receive_message_func_name": "subscriber_connect_to_mqtt_server"},
                                      "WebSocket": {"send_message_func_name": "asyncio_run_send_message_to_websocket_server",
                                                    "receive_message_func_name": "asyncio_run_receive_message_from_device"},
                                      "Modbus": {"send_message_func_name": "send_message_to_device_through_serial",
                                                 "receive_message_func_name": "receive_message_from_device_through_serial"}}
        self.logger = Logger("Channel")

    def send_message_to_server(self, protocol_type, message):
        '''
        channel发送信息
        :return:
        '''
        if protocol_type not in self.protocol_type_dict:
            return self.logger.error("Unknown protocol_type")
        channel_class_info = self.protocol_type_dict[protocol_type]
        channel_class = globals()[channel_class_info["class"]]
        kwargs = {key: var for key, var in channel_class_info.items() if key != 'class'}
        channel = channel_class(**kwargs)
        send_message = getattr(channel, self.channel_function_dict[protocol_type]['send_message_func_name'])
        return send_message(self.device_id, message)

    def get_message_from_device(self, protocol_type):
        '''
        channel接收消息
        :return:
        '''
        if protocol_type not in self.protocol_type_dict:
            return self.logger.error("Unknown protocol_type")
        channel_class_info = self.protocol_type_dict[protocol_type]
        channel_class = globals()[channel_class_info["class"]]
        kwargs = {key: var for key, var in channel_class_info.items() if key != "class"}
        channel = channel_class(**kwargs)
        receive_message = getattr(channel, self.channel_function_dict[protocol_type]["receive_message_func_name"])
        return receive_message(self.device_id)


if __name__ == "__main__":
    mqtt = Channel("A")
    mqtt.send_message_to_server("MQTT", "for MQ")
    # mqtt.get_message_from_device("MQTT")













