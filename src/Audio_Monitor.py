import pyaudio
import wave
import signal
import sys

CHUNK = 1024
FORMAT = pyaudio.paInt16 #TODO: CHeck out what this means
CHANNELS = 1
RATE = 44100

def signal_handler(signal, frame):
        print 'Goodbye'
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

running = True

p = pyaudio.PyAudio()
stream = p.open(
	format = FORMAT,
	channels = CHANNELS,
	rate = RATE,
	input = True,
	frames_per_buffer = CHUNK
	)

frames = []

# for i in range(int(RATE/CHUNK *))

while running:
	data = stream.read(CHUNK)

