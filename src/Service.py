from Audio_Monitor import *
import sys
import signal
import pyaudio

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
BUFFER_SIZE = 128

OUTPUT_FILE = "data.csv"
THRESHOLD = 70

SERVER_ADDRESS = "http://128.122.151.183:3000"

# Add signal listener
def signal_handler(signal, frame):
        print ('Goodbye')
        sys.exit(0)


 # debug
'''c = Communicator("http://128.122.151.183:3000/Session/J-Room/Update/")
print (c, " launched")
data = {
    'updates': [{
        'measureName': 'Sound',
        'timeStamp': int(time.time()),
        'value': int(self.buffer_array[0])}]}
c.sendData(message=data)
print ("Data sent")'''
# /debug


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

    print(stream.read(CHUNK))
    with ByteBuffer(size=BUFFER_SIZE, output_file=OUTPUT_FILE) as buf:
        with Session(address=SERVER_ADDRESS, name="J-Room") as sesh:
            while True:
                print '.',
                data = get_amplitude(stream.read(CHUNK))
                buf.add(sum(imap(int, data)) / len(data))  # integer division
                maxValue = max(data)
                logScale = math.log1p(maxValue) * 22 # TODO: Remove Magic number
                if logScale >= THRESHOLD:
                    print ("Clip : %d" % logScale)


if __name__ == '__main__':
    main()
