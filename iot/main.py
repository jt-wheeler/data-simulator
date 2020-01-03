import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
import argparse
import time
import random
import logging
import string
import numpy as np
import json


async def main(host_name, device_id, shared_access_key, interval):
    connection_string = 'HostName={};DeviceId={};SharedAccessKey={}'.format(
        host_name, device_id, shared_access_key)

    if interval > 0:
        while True:
            await send_message(connection_string)
            time.sleep(interval)
    else:
        await send_message(connection_string)


async def send_message(connection_string):
    device_client = IoTHubDeviceClient.create_from_connection_string(
        connection_string)

    await device_client.connect()

    try:
        message = create_random_message()
        logging.info(message)
        logging.info("Sending message...")
        await device_client.send_message(message)
        logging.info("Message successfully sent!")
    finally:
        await device_client.disconnect()


def create_random_message():
    d = {
        'A': random.randint(0, 100000),
        'B': random.random(),
        'C': {
            'D': random.randint(50, 200),
            'E': random_string(32)
        },
        'F': list(np.random.normal(loc=123, scale=5.6, size=random.randint(1, 100))),
        'G': random_string(15)
    }

    return json.dumps(d)


def random_string(max_length):
    length_of_string = random.randint(1, max_length)
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(0, length_of_string)])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='IoT device simulator.')
    parser.add_argument('--host_name', help='IoT Hub host name')
    parser.add_argument('--device_id', help='IoT Hub Device ID')
    parser.add_argument('--shared_access_key',
                        help='IoT Hub Shared access key.')
    parser.add_argument('--interval', help='Interval at which messages should be transmitted in seconds. If not provided, will only send one message and exit.',
                        default=0)
    parser.add_argument('--log_file',
                        default=None,
                        help='File to write log messages to. Messages will be written to the console if this arg is not provided.')
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
        level=logging.INFO,
        filename=args.log_file
    )

    host_name = args.host_name
    device_id = args.device_id
    shared_access_key = args.shared_access_key
    interval = int(args.interval)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        main(host_name, device_id, shared_access_key, interval))
    loop.close()
