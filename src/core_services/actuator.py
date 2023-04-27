import time
import asyncio
import threading
import concurrent.futures

from common.websocket_enum import WebsocketEnum
from core_services.channels import Channel
from core_services.websocket_channel import WebSocketChannel
from util.logger_manager_ment import Logger


class Actuator:

    def __init__(self):
        '''
        执行器模块，用于拉起服务器进程和监听进程
        :return:
        '''
        self.device_id_list = ["A"]
        self.logger = Logger("Actuator")

    def start_persistent_thread(self, func):
        '''
        用于拉起永久执行的进程并且在其挂掉时重新拉起
        :return:
        '''
        while True:
            try:
                func()
                self.logger.info(str(func) + "start working!")
            except Exception as e:
                self.logger.error(str(func) + "stopped running for " + str(e))
                time.sleep(5)
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
        for device_id in self.device_id_list:
            channel = Channel(device_id)
            for protocol_type in channel.protocol_type_dict.keys():
                receive_message_function_list.append(lambda device_id=device_id, protocol_type=protocol_type: channel.get_message_from_device(protocol_type))
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(receive_message_function_list)) as monitor_actuator:
            futures = [monitor_actuator.submit(self.start_persistent_thread, func) for func in receive_message_function_list]
            for future in concurrent.futures.as_completed(futures):
                if future.result() is None:
                    futures.remove(future)
                    futures.append(monitor_actuator.submit(self.start_persistent_thread, receive_message_function_list[futures.index(future)]))
            monitor_actuator.shutdown(wait=True)


if __name__ == "__main__":
    actuator = Actuator()
    actuator.statr_server_process()
