from Audio_Monitor import *
import sys
import signal
import pyaudio
from math import log1p

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
BUFFER_SIZE = 128

OUTPUT_FILE = "data.csv"
THRESHOLD = 80  # out of 100

SERVER_ADDRESS = "http://128.122.151.163:3000"

# Signal listener to manually stop the program
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
    sesh = Session(address=SERVER_ADDRESS, name="JRoomTest8")
    sesh.begin_session()
    # print(stream.read(CHUNK))
    # with ByteBuffer(size=BUFFER_SIZE, output_file=OUTPUT_FILE) as buf:
    # with Session(address=SERVER_ADDRESS, name="JRoomTest3") as sesh:
    while True:
        data = get_amplitude(stream.read(CHUNK))
         # average with integer division
        avg = sum(imap(int, data)) / len(data)
        sesh.update(measureName="Sound", value=log1p(avg), timeStamp=int(time.time()), description="Hi")


    #             # buf.add(avg)
    #             #FIXME: The average Needs to be in Log Scale
    #             # maxValue = max(data) #FIXME: This is not reading the correct data.
    #             # logScale = log1p(maxValue) * 10 # TODO: Remove Magic number
    #             # if logScale >= THRESHOLD:
    #             #     print ("Clip : %d" % logScale)


if __name__ == '__main__':
    main()
