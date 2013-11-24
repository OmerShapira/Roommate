# import pyaudio
# import wave
import json
import struct
import time
from itertools import imap
from array import array

from urllib2 import urlopen
from urllib import urlencode


# CHUNK = 4096
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# BUFFER_SIZE = 128

# OUTPUT_FILE = "data.csv"
# THRESHOLD = 20000


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
        # self.begin_session()
        pass

    def __exit__(self):
        pass
        # TODO: Is there anything that needs to be done for the session to end?
        # self.disconnect()

    def begin_session(self):
        data = {"name" : self.name}
        print "Sending %s" % data
        send_data(extension='Session/', data=data)

    def send_data(self, extension, data):
        #debug
        # message = urlencode(data)
        message = json.dumps(data)
        print(urlopen(self.address+'/'+extension, message).read())


class ByteBuffer:
    """Buffer for sound objects"""
    def __init__(self, size, output_file):
        # FIXME: unpythonic type checking
        self.size = int(size)
        self.output_file = str(output_file)
        self.pointer = 0

        self.buffer_array = array('i', [0 for i in xrange(self.size)])

    def __enter__(self):
        return self

    def add(self, sample):
        self.buffer_array[self.pointer] = sample
        self.pointer += 1
        if self.pointer >= self.size:
            self.dump()
            self.pointer = 0

    def dump(self, size=None):
        size = size or self.size
        with open(self.output_file, "a+") as out_file:
            out_data = ','.join(imap(str, self.buffer_array))
            out_file.write(out_data)

    def __exit__(self, *args):
        for a in args:
            print(a)
        self.dump(size=self.pointer)
