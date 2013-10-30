import pyaudio
# import wave
import signal
import struct
import sys
from itertools import imap
from array import array

import urllib2


CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 20000
BUFFER_SIZE = 128
OUTPUT_FILE = "data.csv"


# Add signal listener
def signal_handler(signal, frame):
        print ('Goodbye')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


class Communicator:
    """Object for sneding data to the sentient data"""
    def __init__(self, address):
        self.address = address

    def sendData(self, string):
        # TODO: Implement stub


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

    def __exit__(self):
        self.dump(size=self.pointer)


def get_amplitude(sample_block, absolute=True):
    format = "%dh" % (len(sample_block) / 2)
    shorts = struct.unpack(format, sample_block)
    if absolute:
        return [abs(x) for x in shorts]
    else:
        return shorts


def main():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)

    with ByteBuffer(size=BUFFER_SIZE, output_file=OUTPUT_FILE) as buf:
        while True:
            data = get_amplitude(stream.read(CHUNK))
            buf.add(sum(imap(int, data))/len(data))  # integer division
            # print max(data)
            maxValue = max(data)
            if maxValue >= THRESHOLD:
                print ("Clip : %d" % maxValue)


if __name__ == '__main__':
    main()
