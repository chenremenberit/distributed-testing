import asyncio
import threading
import concurrent.futures

from common.websocket_enum import WebsocketEnum
from common.message_format import MessageFormatEnum
from core_services.controller_channel import ControllerChannel
from core_services.websocket_channel import WebSocketChannel
from util.logger_manager_ment import Logger


class Controller:

    def __init__(self):
        '''
        执行器模块，用于拉起服务器进程和监听进程
        :return:
        '''
        self.device_id_list = ["A"]
        self.logger = Logger("Actuator")
        self.command_map = {"A": {"template1": {"protocol": "MQTT", "next_command": "template2"},
                                  "template2": {"protocol": "WebSocket", "next_command": "template1"}}}

    def start_persistent_thread(self, func):
        '''
        用于拉起永久执行的进程并且在其挂掉时重新拉起
        :return:
        '''
        while True:
            try:
                func()
                self.logger.info(str(func) + "start working!")
                break
            except Exception as e:
                self.logger.error(str(func) + "stopped running for " + str(e))
                continue

    def statr_server_process(self):
        '''
        拉起服务器进程
        :return:
        '''
        websocket_server = WebSocketChannel(WebsocketEnum.WEBSOCKET_HOST.value, WebsocketEnum.WEBSOCKET_PORT.value)
        start_websocket_server = websocket_server.start_websocket_server()
        websocket_server_thread = threading.Thread(target=lambda: asyncio.run(start_websocket_server))
        try:
            websocket_server_thread.start()
            self.logger.info("websocket server start working!")
        except Exception as e:
            self.logger.error("websocket server stopped running for " + str(e))
        self.start_monitor_channel_message()
        websocket_server_thread.join()

    def start_monitor_channel_message(self):
        '''
        将所有的需要监听的信息收发增加到线程池中，拉起所有线程池的监听进程
        :return:
        '''
        receive_message_function_list = []
        channel = ControllerChannel()
        for device_id in self.device_id_list:
            for protocol_type in channel.protocol_type_dict.keys():
                receive_message_function_list.append(lambda device_id=device_id, protocol_type=protocol_type:
                                                     channel.get_message_from_device(device_id, protocol_type))
        receive_message_function_list.append(self.process_received_command)
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(receive_message_function_list)) as monitor_actuator:
            futures = [monitor_actuator.submit(self.start_persistent_thread, func) for func in receive_message_function_list]
            concurrent.futures.wait(futures)
            for future in futures:
                if future.result() is None:
                    futures.remove(future)
                    futures.append(monitor_actuator.submit(self.start_persistent_thread, receive_message_function_list[futures.index(future)]))
            monitor_actuator.shutdown(wait=True)

    def process_received_command(self):
        '''
        监听获得的信息，并对其进行处理从而执行下一步的转发操作
        :return:
        '''
        channel = ControllerChannel()
        while True:
            message_list = channel.message_queue.get().splitlines()
            self.logger.info("channel.message_queue get: " + message_list)
            received_element_list = [content.split(": ", maxsplit=1)[1] for content in message_list]
            header = received_element_list[MessageFormatEnum.RECEIVING_HEADER_POSITION.value]
            if header in self.device_id_list:
                received_command = received_element_list[MessageFormatEnum.RECEIVING_COMMAND_POSITION.value]
                if received_command in self.command_map[header]:
                    sending_command = self.command_map[header][received_command]["next_command"]
                    protocol = self.command_map[header][received_command]["protocol"]
                    receiver = received_element_list[MessageFormatEnum.RECEIVING_RECEIVER_POSITION.value]
                    channel.send_message_to_device(protocol, sending_command, receiver)
                else:
                    self.logger.error("Unsupported command: " + received_command + " for " + header)
            else:
                self.logger.error(header + " is not a supported device id!")


if __name__ == "__main__":
    controller = Controller()
    controller.statr_server_process()
