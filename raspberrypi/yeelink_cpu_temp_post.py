import os
import requests
import json
import time
import string


# 获取cpu温度
def getcputemperature():
    cputemp = os.popen('vcgencmd measure_temp').readline()
    sumcputemp = cputemp.replace("temp=","").replace("'C\n","")
    return sumcputemp
