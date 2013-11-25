from Audio_Monitor import *
import sys
import signal
import pyaudio
from math import log1p

CHUNK = 2048
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
    sesh = Session(address=SERVER_ADDRESS, name="JRoom"+str(int(time.time()*1000)))
    with AudioDataBuffer(size=BUFFER_SIZE, output_file=None, output_session=sesh) as buf:
        while True:
            data = get_amplitude(stream.read(CHUNK))
            avg = int(sum(imap(log1p, map(int, data))) / len(data) * MAP_VALUE)
            if DEBUG: 
                print str(avg) + " , ",
            buf.add(int(avg))
            

if __name__ == '__main__':
    main()
