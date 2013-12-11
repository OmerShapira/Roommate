import threading
import time
import json
from urllib2 import urlopen
from urllib import urlencode
import Queue


class DataFollower(threading.Thread):
    ''' Generic class to query objects and send relevant data into a server'''
    def __init__(self, request_address, request_frequency_ms, message_callback):
        self.request_address = request_address
        self.request_frequency_ms = request_frequency_ms
        self.message_callback = message_callback
        super(DataFollower, self).__init__()

    def request(self, **kwargs):
        # TODO: Implement stub
        pass

    def handle_response(self, response):
        # TODO: Implement
        pass

    def run(self):
        response = self.request()
        self.message_callback(self.handle_response(response))
        time.sleep(self.request_frequency_ms * 0.001)


class ZWave(DataFollower):
    """docstring for ZWave"""
    def __init__(self, **kwargs):
        super(ZWave, self).__init__()
        self.kwargs = kwargs

    def request(self, **kwargs):
        requested_time = int(time.time() - super.request_frequency_ms)
        response = urlopen(
            url=super.request_address % requested_time,
            timeout=min(500, super.request_frequency_ms / 2))
        return response.read() or ''

    def handle_response(self, response):
        tree = json.loads(response)
        # TODO : find a way to parse this crap
        pass


class SendQueue(threading.Thread):
    # TODO : See if this need to be a daemon thread
    def __init__(self, api_address, sleep_cycle_ms=10):
        self.queue = Queue.Queue()
        self.api_address = api_address
        self.sleep_cycle_ms = sleep_cycle_ms

    def __enter__(self):
        return self

    def __exit__(self):
        pass

    def put(self, message):
        self.queue.put(message)

    def send(self, message):
        data = urlencode(message)
        urlopen(self.api_address, data)

    def run(self):
        while True:
            while not self.queue.empty():
                self.send(self.queue.get())
            time.sleep(self.sleep_cycle_ms * 0.001)


def main():
    services = []
    with SendQueue(api_address="http://128.122.151.163:3000") as queue:
        for runnable in services:
            # FIXME : non-object oriented
            runnable.message_callback = queue.put
            runnable.start()

if __name__ == '__main__':
    main()
