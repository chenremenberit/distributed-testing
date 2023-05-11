import queue
import asyncio
import websockets

from common.controller_configure import ControllerEnum
from util.logger_manager_ment import Logger


class WebSocketChannel:
    def __init__(self, host, port):
        '''
        通过websockets这个库起一个服务器，在客户端收发消息
        :return:
        '''
        self.host = host
        self.port = port
        self.device_id_list = ["A"]
        self.logger = Logger("WebSocketChannel")
        self.websocket_message_queue = queue.Queue()

    async def websocket_server_receive_message_from_device(self, device_id):
        """
        持续监听含有特定device id的接收消息
        """
        while True:
            try:
                async with websockets.connect("ws://" + self.host + ":" + str(self.port)) as websocket:
                    recv_message = await websocket.recv()
                    message_list = recv_message.splitlines()
                    received_element_list = [content.split(": ", maxsplit=1)[1] for content in message_list]
                    header = received_element_list[ControllerEnum.RECEIVING_HEADER_POSITION.value]
                    if device_id == header:
                        self.websocket_message_queue.put(recv_message)
                        self.logger.info("received message: " + recv_message)
            except websockets.ConnectionClosed as e:
                self.logger.info(e)
                break

    async def send_message_to_websocket_server(self, command, receiver_device_id):
        """
        向服务器端发送消息
        """
        try:
            async with websockets.connect("ws://" + self.host + ":" + str(self.port)) as websocket:
                message = f"command: {command}\r\nprotocol: WebSocket\r\nreceiver: {receiver_device_id}"
                await websocket.send(message)
                recv_message = await websocket.recv()
                self.logger.info("receive message from server :" + recv_message)
                await websocket.close(reason="exit")  # 关闭本次连接
                return True
        except ConnectionRefusedError as e:
            self.logger.error(e)
            return False

    async def start_websocket_server(self):
        """
        启动服务器进程保持一直运行
        """
        async with websockets.serve(self.host, self.port):
            await asyncio.Future()

    def asyncio_run_send_message_to_websocket_server(self, command, receiver_device_id):
        """
        异步运行发送信息的函数
        """
        asyncio.run(self.send_message_to_websocket_server(command, receiver_device_id))

    def asyncio_run_receive_message_from_device(self, device_id):
        """
        异步运行接收信息的函数
        """
        asyncio.run(self.websocket_server_receive_message_from_device(device_id))


if __name__ == "__main__":
    websocket = WebSocketChannel("71.255.2.21", 5678)
    websocket.asyncio_run_send_message_to_websocket_server("template1", "A")
    # websocket.asyncio_run_receive_message_from_device("A")
