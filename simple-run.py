
import config
import signals
import pyaudio
import time

p = pyaudio.PyAudio()
sine = signals.SineWave(config.PERIOD)
lines = []
lines.append(signals.Line(
  config.CH_NOISE_MIC,
  config.CH_SPK_1,
  config.SPK1[0],
  config.SPK1[1]))
lines.append(signals.Line(
  config.CH_NOISE_MIC,
  config.CH_SPK_2,
  config.SPK2[0],
  config.SPK2[1]))

def callback(data, frame_count, time_info, status):
  decoded = signals.decode(data)
  out = [[0]*config.CHUNK for i in range(0,config.CHANNELS)]
  out[config.CH_NOISE_SPK] = sine.get(config.NOISE[0])
  for line in lines:
      out[line.out_channel] = line.process(decoded[line.in_channel])

  return (signals.encode(out), pyaudio.paContinue)

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
