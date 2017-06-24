from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import argparse


class AwsClient(object):
    def __init__(self):
        # Read in command-line parameters
        parser = argparse.ArgumentParser()
        parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host",
                            help="Your AWS IoT custom endpoint")
        parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath",
                            help="Root CA file path")
        parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
        parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
        parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                            help="Use MQTT over WebSocket")
        parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                            help="Targeted client id")
        parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python",
                            help="Targeted topic")

        args = parser.parse_args()
        host = args.host
        rootCAPath = args.rootCAPath
        certificatePath = args.certificatePath
        privateKeyPath = args.privateKeyPath
        useWebsocket = args.useWebsocket
        clientId = args.clientId

        if args.useWebsocket and args.certificatePath and args.privateKeyPath:
            parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
            exit(2)

        if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
            parser.error("Missing credentials for authentication.")
            exit(2)

        # Configure logging
        logger = logging.getLogger("AWSIoTPythonSDK.core")
        logger.setLevel(logging.DEBUG)
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)

        # Init AWSIoTMQTTClient
        self.myAWSIoTMQTTClient = None
        if useWebsocket:
            self.myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
            self.myAWSIoTMQTTClient.configureEndpoint(host, 443)
            self.myAWSIoTMQTTClient.configureCredentials(rootCAPath)
        else:
            self.myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
            self.myAWSIoTMQTTClient.configureEndpoint(host, 8883)
            self.myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

        # AWSIoTMQTTClient connection configuration
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        # Connect and subscribe to AWS IoT
        self.myAWSIoTMQTTClient.connect()

    def subscribe(self, topic, callback):
        self.myAWSIoTMQTTClient.subscribe(topic, 1, callback)

    def publish(self, topic, message):
        self.myAWSIoTMQTTClient.publish(topic, message, 1)
