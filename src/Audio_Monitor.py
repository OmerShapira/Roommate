import pyaudio
import wave
import signal
import struct
import sys
from itertools import imap

from array import array

CHUNK = 4096
FORMAT = pyaudio.paInt32  # TODO: CHeck out what this means
CHANNELS = 1
RATE = 44100
THRESHOLD = 22100
BUFFER_SIZE = 128
OUTPUT_FILE = "data.csv"


# Add signal listener
def signal_handler(signal, frame):
        print ('Goodbye')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


class ByteBuffer:
    """Buffer for sound objects"""
    def __init__(self, size, output_file):
        # FIXME: unpythonic type checking
        self.size = int(size)
        self.output_file = str(output_file)
        # TODO: Allocate output file
        self.pointer = 0

        self.buffer_array = array('h', [0 for i in xrange(self.size)])

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


def amplitude(sample_block):
    count = len(sample_block) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, sample_block)
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
            data = amplitude(stream.read(CHUNK))
            buf.add(sum(imap(int, data))/len(data))  # integer division
            if max(data) >= THRESHOLD:
                print ("ANGRY")


if __name__ == '__main__':
    main()
