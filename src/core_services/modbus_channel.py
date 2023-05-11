import os
import re
import queue
import serial

from common.modbus_enum import ModbusSerialEnum
from util.logger_manager_ment import Logger


class ModBusChannel:
    def __init__(self):
        '''
        Modbus协议交互是通过串口工具将开发板的串口接口连接到PCB的串口专用USB接口上
        :return:
        '''
        self.serial_file_location_dict = {"A": "/dev/ttyUSB0"}
        self.logger = Logger("ModbusController")
        self.modbus_message_queue = queue.Queue()

    def device_connection_status(self, device_sn_code):
        '''
        通过hdc查找设备是否已连接
        :return:
        '''
        device_info = str(os.popen(r"hdc_std list targets"))
        if re.search(device_sn_code, device_info):
            self.logger.info("Device connected !")
            return True
        else:
            self.logger.error("Device disconnected !")
            return False

    def get_serial_file_location_by_device_id(self, device_id):
        '''
        通过device_id来获取serial_file_location
        :return:
        '''
        serial_file_location = self.serial_file_location_dict[device_id]
        return serial_file_location

    def send_message_to_device_through_serial(self, command, receiver_device_id):
        '''
        对指定串口发送消息
        :return:
        '''
        serial_file_location = self.get_serial_file_location_by_device_id(receiver_device_id)
        ser = serial.Serial(port=serial_file_location, baudrate=ModbusSerialEnum.BAND_RATE_ENUM.value,
                            timeout=ModbusSerialEnum.SERIAL_TIMEOUT_ENUM.value)
        message = f"command: {command}\r\nprotocol: Modbus\r\nreceiver: {receiver_device_id}"
        ser.write(message.encode())
        self.logger.info("send message:" + message + " to device")
        ser.close()

    def receive_message_from_device_through_serial(self, device_id):
        '''
        从指定串口接收消息
        :return:
        '''
        serial_file_location = self.get_serial_file_location_by_device_id(device_id)
        ser = serial.Serial(port=serial_file_location, baudrate=ModbusSerialEnum.BAND_RATE_ENUM.value,
                            timeout=ModbusSerialEnum.SERIAL_TIMEOUT_ENUM.value)
        while True:
            try:
                message = str(ser.readlines())
                self.modbus_message_queue.put(message)
                self.logger.info("receive message:" + message + " from device")
            except serial.SerialException:
                self.logger.error("The serial to device: " + device_id + "is abnormal!")


if __name__ == "__main__":
    modbus = ModBusChannel()
    modbus.send_message_to_device_through_serial("template1", "A")
