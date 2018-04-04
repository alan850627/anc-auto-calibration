
import numpy as np
import config
import signals
from avg import RunningAvg
from enum import Enum

class state(Enum):
  STARTED = 0
  MOD_AMP = 1
  MOD_AMP_MAKE_LOUD = 2
  MOD_AMP_MAKE_QUIET = 3

  MOD_PHASE = 4
  MOD_PHASE_DLY = 5
  MOD_PHASE_EXP = 6
  DONE = 7

sine = signals.SineWave(config.PERIOD)
hp1 = signals.HighPass()
hp2 = signals.HighPass()
avg = RunningAvg()

class StateMachine(object):
  def __init__(self):
    self.state = state.STARTED
    self.lines = []
    self.lines.append(signals.Line(
      config.CH_NOISE_MIC,
      config.CH_SPK_1,
      config.SPK1[0],
      config.SPK1[1]))
    self.lines.append(signals.Line(
      config.CH_NOISE_MIC,
      config.CH_SPK_2,
      config.SPK2[0],
      config.SPK2[1]))
    self.counter = 0

  def process(self, data):
    decoded = signals.decode(data)
    out = [[0]*config.CHUNK for i in range(0,config.CHANNELS)]
    out[config.CH_N_SPK] = sine.get(config.NOISE[0])

    for line in self.lines:
        out[line.out_channel] = line.process(decoded[line.in_channel])

    #####################################
    if self.state == state.STARTED:

      if self.counter > 10:
        self.counter = 0
        self.alternate_counter = 0
        self.cycle_counter = 0
        self.mod_line = 0
        self.prev_state = state.MOD_AMP_MAKE_LOUD
        self.state = state.MOD_AMP

        mic1_rms = signals.rms(hp1.process(decoded[config.CH_HEAD_MIC_1]))
        mic2_rms = signals.rms(hp2.process(decoded[config.CH_HEAD_MIC_2]))
        self.prev_sound = max(mic1_rms, mic2_rms)

        print(self.state)

    #####################################
    elif self.state == state.MOD_AMP:
      mic1_rms = signals.rms(hp1.process(decoded[config.CH_HEAD_MIC_1]))
      mic2_rms = signals.rms(hp2.process(decoded[config.CH_HEAD_MIC_2]))
      self.cur_sound = avg.get(max(mic1_rms, mic2_rms))

      if self.counter > 10:
        if (self.cur_sound < config.BASE_SOUND or self.cycle_counter >= config.MAX_CYCLES): 
          self.state = state.DONE
          self.counter = 0

        elif (self.alternate_counter > 4):
          self.cycle_counter += 1
          self.alternate_counter = 0
          self.prev_state = state.MOD_PHASE_DLY
          self.state = state.MOD_PHASE
          print(self.state, self.mod_line, self.cur_sound)

        elif (self.cur_sound < self.prev_sound):
          self.state = self.prev_state
        else:
          self.alternate_counter += 1
          if(self.prev_state == state.MOD_AMP_MAKE_LOUD):
            self.state = state.MOD_AMP_MAKE_QUIET
          else:
            self.state = state.MOD_AMP_MAKE_LOUD

        self.prev_sound = self.cur_sound
        self.counter = 0

    #####################################
    elif self.state == state.MOD_AMP_MAKE_LOUD:
      self.prev_state = state.MOD_AMP_MAKE_LOUD
      line = self.lines[self.mod_line]
      line.amp += 0.002
      print(self.state, self.mod_line, self.cur_sound)
      self.state = state.MOD_AMP

    #####################################
    elif self.state == state.MOD_AMP_MAKE_QUIET:
      self.prev_state = state.MOD_AMP_MAKE_QUIET
      line = self.lines[self.mod_line]
      line.amp -= 0.002
      print(self.state, self.mod_line, self.cur_sound)
      self.state = state.MOD_AMP

    #####################################
    elif self.state == state.MOD_PHASE:
      mic1_rms = signals.rms(hp1.process(decoded[config.CH_HEAD_MIC_1]))
      mic2_rms = signals.rms(hp2.process(decoded[config.CH_HEAD_MIC_2]))
      self.cur_sound = avg.get(max(mic1_rms, mic2_rms))

      if self.counter > 10:
        if (self.cur_sound < config.BASE_SOUND or self.cycle_counter >= config.MAX_CYCLES): 
          self.state = state.DONE
          self.counter = 0

        elif (self.alternate_counter > 4):
          self.alternate_counter = 0
          self.prev_state = state.MOD_AMP_MAKE_QUIET
          self.state = state.MOD_AMP
          self.mod_line = (self.mod_line + 1) % len(self.lines)
          print(self.state, self.mod_line, self.cur_sound)

        elif (self.cur_sound < self.prev_sound):
          self.state = self.prev_state
        else:
          self.alternate_counter += 1
          if(self.prev_state == state.MOD_PHASE_DLY):
            self.state = state.MOD_PHASE_EXP
          else:
            self.state = state.MOD_PHASE_DLY

        self.prev_sound = self.cur_sound
        self.counter = 0

    #####################################
    elif self.state == state.MOD_PHASE_DLY:
      self.prev_state = state.MOD_PHASE_DLY
      self.lines[self.mod_line].delay()
      print(self.state, self.mod_line, self.cur_sound)
      self.state = state.MOD_PHASE

    #####################################
    elif self.state == state.MOD_PHASE_EXP:
      self.prev_state = state.MOD_PHASE_EXP
      line = self.lines[self.mod_line].expedite()
      print(self.state, self.mod_line, self.cur_sound)
      self.state = state.MOD_PHASE

    #####################################
    elif self.state == state.DONE:
      if self.counter > 300:
        self.counter = 0
        mic1_rms = signals.rms(hp1.process(decoded[config.CH_HEAD_MIC_1]))
        mic2_rms = signals.rms(hp2.process(decoded[config.CH_HEAD_MIC_2]))
        print("Mic 1: %d, Mic 2: %d" %(mic1_rms, mic2_rms))
        for i, line in enumerate(self.lines):
          print("Line %d, Amp: %d, Dly: %d" %(i, line.amp, line.dly))        


    self.counter += 1
    return signals.encode(out)