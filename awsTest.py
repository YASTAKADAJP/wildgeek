'''
Send Time Sample
2019/2/16
Programmed by Y.Takada
'''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import datetime
import logging

# select Debug mode
_DEBUG_ = 'PC'
#_DEBUG_ = 'Raspberry'

# Setup Param
host = "xxxxxxxxxxxxxx.iot.ap-northeast-1.amazonaws.com"

if _DEBUG_ == 'PC':
    #for PC
    rootCAPath = "C:/Projects/python/awsTest/cert/AmazonRootCA1.pem"
    certificatePath = "C:/Projects/python/awsTest/cert/xxxxxxxxx-certificate.pem.crt"
    privateKeyPath = "C:/Projects/python/awsTest/cert/xxxxxxxxx-private.pem.key"
else:
    #for Raspberry Pi
    rootCAPath = "/cert/AmazonRootCA1.pem"
    certificatePath = "/cert/xxxxxxxxx-certificate.pem.crt"
    privateKeyPath = "/cert/xxxxxxxxx-private.pem.key"

useWebsocket = False
clientId = "test"
topic = "test/time"

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, 443)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)      # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)            # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)    # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)         # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
time.sleep(2)
# Initial

try:
    while True:
        nowtime = datetime.datetime.now()
        nowsettime = int(time.mktime(nowtime.timetuple()))  # UNIX Time
        #send Command
        message = {}
        message['time'] = "Test"
        message['ttl']  = nowsettime + 2592000
        messageJson = json.dumps(message)
        print (messageJson)
        myAWSIoTMQTTClient.publish(topic, messageJson, 1)
        time.sleep(10)
except:
    import traceback
    traceback.print_exc()

print ("Terminated")
