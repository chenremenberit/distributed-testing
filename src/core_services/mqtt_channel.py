import paho.mqtt.client as mqtt

from common.mqtt_enum import CommonEnum
from common.mqtt_enum import MQTTReturnCode
from common.mqtt_enum import MQTTServerEnum
from util.logger_manager_ment import Logger


class MQTTChannel:
    def __init__(self, host, port, client_id):
        '''
        与MQTT服务器交互的channel，主机可执行的包括发布者的操作、订阅者的操作
        :return:
        '''
        self.host = host
        self.port = port
        self.client_id = client_id
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.on_connect = self.subscriber_connect_to_mqtt_server_status
        self.client.on_message = self.subscriber_receive_message_from_mqtt_server
        self.logger = Logger("MQTTChannel")

    def subscriber_connect_to_mqtt_server_status(self,  client, userdata, flags, rc):
        '''
        查询连接状态，判断是否是否能正常连接服务器
        :return:
        '''
        topic = "test"
        if str(rc) == MQTTReturnCode.CONNECTION_SUCCESS.value:
            self.client.subscribe(topic)
        else:
            self.logger.error("Connection rejected, Connected with result code " + str(rc))

    def subscriber_receive_message_from_mqtt_server(self, client, userdata, msg):
        '''
        获取订阅获得的信息
        :return: msg
        '''
        self.logger.info(msg.topic + " " + str(msg.payload))
        return msg

    def subscriber_connect_to_mqtt_server(self, topic):
        '''
        订阅者连接到服务器
        :return: msg
        '''
        self.client.username_pw_set(MQTTServerEnum.MQTT_SERVER_USERNAME.value, MQTTServerEnum.MQTT_SERVER_PASSWORD.value)
        self.client.connect(self.host, self.port, CommonEnum.MQTT_TIMEOUT_ENUM.value)
        self.client.subscribe(topic)
        self.client.loop_forever()

    def publish_message_to_mqtt_server(self, topic, message):
        '''
        发布者向MQTT服务器发布消息
        :return:
        '''
        self.client.username_pw_set(MQTTServerEnum.MQTT_SERVER_USERNAME.value, MQTTServerEnum.MQTT_SERVER_PASSWORD.value)
        self.client.connect(self.host, self.port, CommonEnum.MQTT_TIMEOUT_ENUM.value)
        self.client.loop_start()
        self.client.publish(topic, message)
        self.client.loop_stop()
        self.client.disconnect()


if __name__ == "__main__":
    mqtt = MQTTChannel("71.255.2.21", 1883, "subscriber1")
    mqtt.subscriber_connect_to_mqtt_server("A")