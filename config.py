

WIDTH = 2
CHANNELS = 4
RATE = 44100
CHUNK = 2048

CH_HEAD_MIC_1 = 0
CH_HEAD_MIC_2 = 1
CH_NOISE_MIC = 2

CH_SPK_1 = 0
CH_SPK_2 = 1
CH_NOISE_SPK = 2

# (amp, dly)
NOISE=(32000,0)
SPK1=(0,9)
SPK2=(-0.450,15)
# SPK1=(0,0)
# SPK2=(0,0)

FREQ = 1000
PERIOD = RATE/float(FREQ)
BASE_SOUND = 300
MAX_CYCLES = 20