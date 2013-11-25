from Audio_Monitor import *
import sys
import signal
import pyaudio
from math import log1p, exp, e, sqrt
from time import localtime, strftime

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
BUFFER_SIZE = 128
MAP_VALUE = 10
DEBUG = False
OUTPUT_FILE = "data.csv"
THRESHOLD = 80  # out of 100

SERVER_ADDRESS = "http://128.122.151.163:3000"


# Signal listener to manually stop the program
def signal_handler(signal, frame):
        print ('Goodbye')
        sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    print("Hello")
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)
    now = strftime("%Y-%m-%d-%H-%M-%S", localtime())
    compress = lambda x: 100.0/(1 + exp(-4 * e * (x/100 - 0.4)))
    sesh = Session(address=SERVER_ADDRESS, name="JRoom-"+now)
    with AudioDataBuffer(size=BUFFER_SIZE, output_file=None, output_session=sesh) as buf:
        while True:
            data = get_amplitude(stream.read(CHUNK))
            logs = imap(log1p, data)
            logs_amplified = imap(lambda x: x*MAP_VALUE, logs)
            squares = imap(lambda x: x*x, logs_amplified)
            rms = sqrt(sum(squares)/len(data))
            compressed = int(compress(rms))
            if DEBUG:
                print str(compressed) + " , ",
            buf.add(compressed)
            

if __name__ == '__main__':
    main()
