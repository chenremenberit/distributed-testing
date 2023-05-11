import queue
import asyncio
import websockets

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

    async def shake_hands_with_server(self, device_id, websocket):
        """
        握手，通过发送deivice_id，接收连接成功消息来进行双方的握手。
        若成功，则跳出循环，结束函数；若失败，则继续发送device_id.
        """
        while True:
            await websocket.send(device_id)
            response_str = await websocket.recv()
            if response_str == (device_id + " is already connected to the server"):
                self.logger.info("connection on")
                return True

    async def server_shake_hands_with_device(self, websocket):
        """
        握手，通过接收对应设备的device_id标识信息，来回应对应的信息
        """
        while True:
            recv_message = await websocket.recv()
            self.logger.info("receive message from:" + recv_message)
            for device_id in self.device_id_list:
                if recv_message == device_id:
                    self.logger.info("The connection to device " + device_id + " is normal")
                    await websocket.send(device_id + " is already connected to the server")
                    return True

    async def receive_message_and_reply(self, websocket):
        """
        接收从客户端发来的消息并处理，再回复客户端。
        """
        while True:
            try:
                await self.server_shake_hands_with_device(websocket)
                recv_message = await websocket.recv()
                self.logger.info("server receive message: " + recv_message)
                await websocket.send("The server has received you message: " + recv_message)
                return recv_message
            except websockets.ConnectionClosed as e:
                self.logger.info(e)
                break

    async def websocket_server_receive_message_from_device(self, device_id):
        """
        持续监听含有特定device id的接收消息
        """
        while True:
            try:
                async with websockets.connect("ws://" + self.host + ":" + str(self.port)) as websocket:
                    await self.shake_hands_with_server(device_id, websocket)
                    await self.server_shake_hands_with_device(websocket)
                    recv_message = await websocket.recv()
                    self.websocket_message_queue.put(recv_message)
                    if recv_message.startswith(device_id):
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
                await self.shake_hands_with_server(receiver_device_id, websocket)
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
        async with websockets.serve(self.receive_message_and_reply, self.host, self.port):
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
