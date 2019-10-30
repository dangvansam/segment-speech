import os
from time import sleep
import  csv
import numpy as np
from pydub import AudioSegment
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import librosa
from inaSpeechSegmenter import Segmenter, seg2csv
import  wave
import audioop
import scipy
from datetime import datetime

def removeMusicAndCut(file_name, out_dir):
  print('\nREMOVE MUSIC AND CUT')
  seg = Segmenter()
  segmentation = seg(file_name)
  sample_rate, raw_audio = scipy.io.wavfile.read(file_name)
  speech = []
  print(segmentation)
  count = 1
  if not os.path.exists(out_dir):
    os.mkdir(out_dir)
  for s in segmentation:
    if s[0] != 'Music' and s[0] != 'NOACTIVITY':
      #speech.append(s)
      print(str(count),'dur of sen:',s[2]-s[1])
      speech_data = raw_audio[int(s[1]*sample_rate):int(s[2]*sample_rate)]
      speech_data = np.array(speech_data)

      print(len(speech_data), len(speech_data)/sample_rate)
      if len(speech_data)/sample_rate < 1.0 or len(speech_data)/sample_rate > 10:
        continue
      else:
        scipy.io.wavfile.write(out_dir + '/' + file_name.split('/')[-1].replace('.wav','') + '_' + str(count) + '.wav', sample_rate, speech_data)
        count += 1

d = 'thai_son_data'
for f in os.listdir(d):
    print(f)
    removeMusicAndCut(d+'/'+f,d+ '_cuted')