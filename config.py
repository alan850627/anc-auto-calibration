# GLOBALS
WIDTH = 2
CHANNELS = 4
RATE = 44100
CHUNK = 2048

CH_HEAD_MIC_1 = 0
CH_HEAD_MIC_2 = 1
CH_NOISE_MIC = 2

CH_SPK_1 = 0
CH_SPK_2 = 1
CH_N_SPK = 2

# WIDTH = 2
# CHANNELS = 2
# RATE = 44100
# CHUNK = 1024

# CH_HEAD_MIC_1 = 0
# CH_HEAD_MIC_2 = 1
# CH_NOISE_MIC = 0

# CH_SPK_1 = 1
# CH_SPK_2 = 1
# CH_N_SPK = 0

# (amp, dly)
NOISE=(5000,0)
SPK1=(0,101)
SPK2=(0,126)

FREQ = 800
PERIOD = int(RATE/FREQ) 
BASE_SOUND = 250
MAX_CYCLES = 20