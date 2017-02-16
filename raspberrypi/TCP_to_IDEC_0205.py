from pymodbus3.client.sync import ModbusTcpClient as ModbusClient
from pymodbus3.transaction import ModbusSocketFramer as ModbusFramer
import threading
import logging
import time
import paho.mqtt.client as mqtt
import json


# <editor-fold desc="mqtt callback">
def on_fpq_do_hx_message(client, userdata, msg):
    print("msg:" + str(msg.payload))
    # rsv_data = int(msg.payload)
    # print(rsv_data)
    if int(msg.payload) == 1:
        rq = modbus_client.write_coils(0, [True] * 1, unit=0x01)
    elif int(msg.payload) == 0:
        rq = modbus_client.write_coils(0, [False] * 1, unit=0x01)


def on_fpq_do_sbf_message(client, userdata, msg):
    if msg.payload == "1":
        rq = modbus_client.write_coils(1, [True] * 1, unit=0x01)
    elif msg.payload == "0":
        rq = modbus_client.write_coils(1, [False] * 1, unit=0x01)


def on_message(client, userdata, msg):
    print("topic:" + msg.topic + " Message:" + str(msg.payload) + "with QoS" + str(msg.qos))


def on_publish(msg, rc):  # 成功发布消息的操作
    if rc == 0:
        print("publish success, msg = " + msg)


def on_connect(client, userdata, flags, rc):  # 连接后的操作 0为成功
    if rc == 0:
        print("Connection successful")
        client.subscribe("one2one/fpq/#", qos=1)  # qos
    else:
        print("Error:Connection returned " + str(rc))
# </editor-fold>


mqtt_client = mqtt.Client(
    client_id="paho-fpq-client",  # 用来标识设备的ID，用户可自己定义，在同一个实例下，每个实体设备需要有一个唯一的ID
    clean_session=True,
    userdata=None,
    protocol='MQTTv311'
)

# trust = "E:\root_cert.pem"  # 开启TLS时的认证文件目录
user = "ds11-01/fpq"
pwd = "Zw7VEoAXBwl+YxZm+Kw81cU9cMzMk4k4m+C4FgTvsXM="
endpoint = "ds11-01.mqtt.iot.gz.baidubce.com"
port = 1883
topic = "one2one/fpq"

# 防喷器数字量输出 回调
mqtt_client.message_callback_add("one2one/fpq/hx", on_fpq_do_hx_message)
mqtt_client.message_callback_add("one2one/fpq/sbf", on_fpq_do_sbf_message)

# client.tls_insecure_set(True)  # 检查hostname的cert认证
# client.tls_set(trust)  # 设置认证文件
# mqtt_client.username_pw_set(user, pwd)  # 设置用户名，密码
# mqtt_client.connect(endpoint, port, 60)  # 连接服务 keepalive=60
# mqtt_client.on_connect = on_connect  # 连接后的操作
# mqtt_client.on_message = on_message
# mqtt_client.loop_start()
# time.sleep(2)

received_discrete_inputs_data = [False]*8


def compare_update_di_list(old_list, new_list):
    for i in range(0, len(new_list)):
        if old_list[i] == new_list[i]:
            pass
        else:  # 两个列表对应元素不同，则输出对应的索引
            print("update bytes[%d];" %i +"value=" + str(new_list[i]))
    old_list = new_list


class ModbusTcpToIDEC:
    def __init__(self, devname, di_channel):
        self.lastval = [False]*di_channel
        self.devname = devname

    def poll(self):
        try:
            rr = modbus_client.read_discrete_inputs(0, 8, unit=0x01)
            for i in range(0, len(rr.bits)):
                if self.lastval[i] == rr.bits[i]:
                    pass
                else:
                    print("update bytes[%d];" % i + "value=" + str(rr.bits[i]))
                    # send msg to mqtt broker
                    fulltopic = "one2one/" + self.devname
            self.lastval = rr.bits
        except Exception as exc:
            print("Error reading " + ": %s", exc)


def modbus_rr():
    # while threads_switch:
    rr = modbus_client.read_discrete_inputs(0, 8, unit=0x01)
    global received_discrete_inputs_data
    compare_update_di_list(received_discrete_inputs_data, rr.bits)
    # print("list response:" + str(rr.bits))
    # print(int(rr.bits[2]))


# global read_discrete_inputs_data
# read_discrete_inputs_data = rr.bits
#  modbus_client.write_coils(0, write_coils_data, unit=0x01)


def modbus_print():
    global threads_switch
    while threads_switch:
        global read_discrete_inputs_data
        global discrete_inputs_data
        if discrete_inputs_data != read_discrete_inputs_data:
            msg = str(read_discrete_inputs_data)
            rc, mid = mqtt_client.publish("one2one/fpq", payload=msg, qos=1)  # qos
            on_publish(msg, rc)
            print(read_discrete_inputs_data)
            discrete_inputs_data = read_discrete_inputs_data


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.CRITICAL)

modbus_client = ModbusClient('192.168.1.133', port=502, retries=2, framer=ModbusFramer)
# modbus_client.close()
modbus_client.connect()

write_coils_data = []

discrete_inputs_data = []
threads_switch = 1
idecrr = ModbusTcpToIDEC("fpq", 8)
while True:
    idecrr.poll()
    # time.sleep(1)


#
# threads = []
# t1 = threading.Thread(target=modbus_rr)
# threads.append(t1)
# t2 = threading.Thread(target=modbus_print)
# threads.append(t2)
#
# for t in threads:
#     t.setDaemon(True)
#     t.start()
#
# for i in range(60):
#     time.sleep(1)
#     print(i)
#
# threads_switch = 0
# modbus_client.close()

