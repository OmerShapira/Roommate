import json
import struct
import time
from itertools import imap
from array import array
from math import log1p
from urllib2 import Request, urlopen


def get_amplitude(sample_block, absolute=True):
    format = "%dh" % (len(sample_block) / 2)
    shorts = struct.unpack(format, sample_block)
    if absolute:
        return [abs(x) for x in shorts]
    else:
        return shorts


class Session:
    """
    Object for sending data to the sentient data.
    Will begin a session when called as 'with'
    """
    def __init__(
            self,
            address="http://128.122.151.183:3000",
            name=None):
            self.address = address
            self.name = name or "Unnamed Session at %s" % time.strftime("%a, %d %b %Y %H:%M:%S")

    def __enter__(self):
        self.begin_session()

    def __exit__(self):
        pass
        # TODO: Is there anything that needs to be done for the session to end?
        # self.disconnect()

    def send_data(self, extension, data):
        message = json.dumps(data)
        req = Request(self.address+'/'+extension, message, {'Content-Type': 'application/json'})
        urlopen(req)
        # print(urlopen()

    def begin_session(self):
        data = {"name": self.name}
        print "Sending %s" % data
        self.send_data(extension='Session/', data=data)

    def update(self, measureName, value, timeStamp=None, description=''):
        # FIXME: Is this the correct time format?
        timeStamp = timeStamp or int(round(time.time() * 1000))
        data = {"updates": [{
            "measureName": measureName,
            "value": value,
            "timeStamp": timeStamp,
            "description": description
        }]}
        self.send_data(extension='Session/' + self.name + '/Update',
                       data=data)


class AudioDataBuffer:
    """Buffer for sound objects"""
    def __init__(self, size, output_file=None, output_session=None):
        # FIXME: unpythonic type checking
        self.size = int(size)
        self.output_file = str(output_file) if output_file else None
        if output_session:
            self.output_session = output_session
            self.output_session.begin_session()
        self.pointer = 0

        self.buffer_array = array('i', [0 for i in xrange(self.size)])

    def __enter__(self):
        # TODO: Maybe init here?
        return self

    def add(self, sample):
        self.buffer_array[self.pointer] = sample
        self.pointer += 1
        if self.pointer >= self.size:
            if self.output_file:
                self.dumpToFile()
            if self.output_session:
                self.dumpToSession()
            self.pointer = 0

    def get_average_RMS(self, size=None):
        size = size or self.size
        rms = sum(self.buffer_array[:size]) / size
        return rms

    def dumpToSession(self, size=None):
        rms = self.get_average_RMS(size=size)
        print " ->  Sent: "+str(rms)
        if self.output_session:
            self.output_session.update(
                measureName="Sound", value=rms)

    def dumpToFile(self, size=None):
        with open(self.output_file, "a+") as out_file:
            # out_data = ','.join(imap(str, self.buffer_array))
            out_data = self.get_average_RMS(size=size)
            out_file.write(out_data)

    def __exit__(self, *args):
        for a in args:
            print(a)
        if self.output_file:
            self.dumpToFile(size=self.pointer)
        if self.output_session:
            self.dumpToSession(size=self.pointer)
