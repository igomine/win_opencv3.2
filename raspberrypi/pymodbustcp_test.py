from pymodbus3.client.sync import ModbusTcpClient as ModbusClient
from pymodbus3.transaction import ModbusSocketFramer as ModbusFramer
import threading
import logging
import time
import paho.mqtt.client as mqtt
import datetime

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.CRITICAL)

modbus_client = ModbusClient('192.168.1.133', port=503, retries=2, framer=ModbusFramer)
modbus_client.connect()

write_coils_data = []
read_discrete_inputs_data = []
discrete_inputs_data = []
threads_switch = 1


def modbus_rr():
    global threads_switch
    while threads_switch:
        rr = modbus_client.read_discrete_inputs(0, 8, unit=0x01)
        global read_discrete_inputs_data
        read_discrete_inputs_data = rr.bits
        modbus_client.write_coils(0, write_coils_data, unit=0x01)


def modbus_print():
    global threads_switch
    while threads_switch:
        global read_discrete_inputs_data
        global discrete_inputs_data
        if discrete_inputs_data != read_discrete_inputs_data:
            msg = str(read_discrete_inputs_data)
            rc, mid = mqtt_client.publish(topic, payload=msg, qos=1)  # qos
            on_publish(msg, rc)
            print(read_discrete_inputs_data)
            discrete_inputs_data = read_discrete_inputs_data


def on_publish(msg, rc):  # 成功发布消息的操作
    if rc == 0:
        print("publish success, msg = " + msg)


def on_connect(client, userdata, flags, rc):  # 连接后的操作 0为成功
    print("Connection returned " + str(rc))


mqtt_client = mqtt.Client(
    client_id="test_mqtt_sender_1",  # 用来标识设备的ID，用户可自己定义，在同一个实例下，每个实体设备需要有一个唯一的ID
    clean_session=True,
    userdata=None,
    protocol='MQTTv311'
)

# trust = "E:\root_cert.pem"  # 开启TLS时的认证文件目录
user = "ds11-01/zlq"
pwd = "4MnBAZJy9XBqhbgrk05F1PFjS718d8PFVlr+jqqLo9o="
endpoint = "ds11-01.mqtt.iot.gz.baidubce.com"
port = 1883
topic = "one2one/zlq"

# client.tls_insecure_set(True)  # 检查hostname的cert认证
# client.tls_set(trust)  # 设置认证文件
mqtt_client.username_pw_set(user, pwd)  # 设置用户名，密码
mqtt_client.connect(endpoint, port, 60)  # 连接服务 keepalive=60
mqtt_client.on_connect = on_connect  # 连接后的操作
mqtt_client.loop_start()
time.sleep(2)
'''
5
count = 0
while count < 5:  # 发布五条消息
    count = count + 1
    msg = str(datetime.datetime.now())
    rc, mid = client.publish(topic, payload=msg, qos=1)  # qos
    on_publish(msg, rc)
    time.sleep(2)
'''
threads = []
t1 = threading.Thread(target=modbus_rr)
threads.append(t1)
t2 = threading.Thread(target=modbus_print)
threads.append(t2)

for t in threads:
    t.setDaemon(True)
    t.start()

for i in range(60):
    time.sleep(1)
    print(i)

threads_switch = 0
modbus_client.close()


'''

test = []
while True:
    rr = modbus_client.read_discrete_inputs(0, 8, unit=0x05)
    if rr.bits != test:
        print(rr.bits)
        msg = str(rr.bits)
        rc, mid = mqtt_client.publish(topic, payload=msg, qos=1)  # qos
        test = rr.bits
    # time.sleep(0.5)

rr = modbus_client.read_discrete_inputs(0, 8, unit=0x05)


rq = modbus_client.write_coils(0, [True]*8, unit=0x01)

rr = modbus_client.read_coils(0, 8, unit=0x02)


#---------------------------------------------------------------------------#
# specify slave to query
#---------------------------------------------------------------------------#
# The slave to query is specified in an optional parameter for each
# individual request. This can be done by specifying the `unit` parameter
# which defaults to `0x00`
#---------------------------------------------------------------------------#
rr = modbus_client.read_coils(1, 1, unit=0x02)



#---------------------------------------------------------------------------#
# example requests
#---------------------------------------------------------------------------#
# simply call the methods that you would like to use. An example session
# is displayed below along with some assert checks. Note that some modbus
# implementations differentiate holding/input discrete/coils and as such
# you will not be able to write to these, therefore the starting values
# are not known to these tests. Furthermore, some use the same memory
# blocks for the two sets, so a change to one is a change to the other.
# Keep both of these cases in mind when testing as the following will
# _only_ pass with the supplied async modbus server (script supplied).
#---------------------------------------------------------------------------#
rq = modbus_client.write_coil(6, True)
rr = modbus_client.read_coils(6,1)
assert(rq.function_code < 0x80)     # test that we are not an error
assert(rr.bits[0] == True)          # test the expected value

rq = modbus_client.write_coils(1, [True]*8)
rr = modbus_client.read_coils(1,8)
assert(rq.function_code < 0x80)     # test that we are not an error
assert(rr.bits == [True]*8)         # test the expected value

rq = modbus_client.write_coils(1, [False]*8)
rr = modbus_client.read_discrete_inputs(1,8)
assert(rq.function_code < 0x80)     # test that we are not an error
assert(rr.bits == [False]*8)         # test the expected value

rq = modbus_client.write_register(1, 10)
rr = modbus_client.read_holding_registers(1,1)
assert(rq.function_code < 0x80)     # test that we are not an error
assert(rr.registers[0] == 10)       # test the expected value

rq = modbus_client.write_registers(1, [10]*8)
rr = modbus_client.read_input_registers(1,8)
assert(rq.function_code < 0x80)     # test that we are not an error
assert(rr.registers == [10]*8)      # test the expected value

arguments = {
    'read_address':    1,
    'read_count':      8,
    'write_address':   1,
    'write_registers': [20]*8,
}
rq = modbus_client.readwrite_registers(**arguments)
rr = modbus_client.read_input_registers(1,8)
assert(rq.function_code < 0x80)     # test that we are not an error
assert(rq.registers == [20]*8)      # test the expected value
assert(rr.registers == [20]*8)      # test the expected value

#---------------------------------------------------------------------------#
# close the client
#---------------------------------------------------------------------------#
modbus_client.close()
'''