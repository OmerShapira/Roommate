import pyaudio
import wave
import signal
import sys

from array import array

CHUNK = 4096
FORMAT = pyaudio.paInt16 #TODO: CHeck out what this means
CHANNELS = 1
RATE = 44100

# Add signal listener
def signal_handler(signal, frame):
        print ('Goodbye')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

p = pyaudio.PyAudio()
buf = ByteBuffer()

stream = p.open(
	format = FORMAT,
	channels = CHANNELS,
	rate = RATE,
	input = True,
	frames_per_buffer = CHUNK
	)

while True:
	data = stream.read(CHUNK)
	buf.add(sum(data)/CHUNK) #integer division


class ByteBuffer:
	"""Buffer for sound objects"""
	def __init__(self, size, output_file):
		# FIXME: unpythonic type checking
		self.size = int(size)
		self.output_file = str(output_file)
		# TODO: Allocate output file
		self.pointer = 0

		self.buffer_array = array('I', [0 for i in xrange(self.size)])
	

	def add(self,sample):
		self.buffer_array[self.pointer] = sample
		self.pointer += 1
		if self.pointer >= self.size:
			dump()
			self.pointer = 0


	def dump()