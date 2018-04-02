from state import StateMachine
import config
import pyaudio
import time

machine = StateMachine()
p = pyaudio.PyAudio()

def callback(data, frame_count, time_info, status):
  out = machine.process(data)
  return (out, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(config.WIDTH),
                channels=config.CHANNELS,
                rate=config.RATE,
                frames_per_buffer=config.CHUNK,
                input=True,
                output=True,
                stream_callback=callback)

stream.start_stream()

while True:
  time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()
