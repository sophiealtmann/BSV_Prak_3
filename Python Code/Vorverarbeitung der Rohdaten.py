import numpy as np
from scipy import fftpack
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
import Lab3Functions as lf3
import Functions as fun

# Daten importieren
weights,mvc,fatigue=lf3.import_data(";")

mvc_time=mvc.t.to_numpy
# Offset eliminieren
mvc_offset= fun.eliminateoffset(mvc.emg, mvc.t)

# Filtern zwischen 20 und 450 Hz
mvc_filtered = fun.filter(mvc_offset, mvc.t)

# Gleichrichten des Signals
mvc_gleich = fun.gleich(mvc_offset, mvc.t, mvc_filtered)

# Einhüllende bilden
mvc_env=fun.huelle(mvc_offset, mvc.t, mvc_gleich, 3)


weights_offset=fun.eliminateoffset(weights.emg, weights.t)
fatigue_offset=fun.eliminateoffset(fatigue.emg, fatigue.t)

weights_filtered=fun.filter(weights_offset,weights.t)
fatigue_filtered=fun.filter(fatigue_offset,fatigue.t)

weights_gleich=fun.gleich(weights_offset, weights.t, weights_filtered)
fatigue_gleich=fun.gleich(fatigue_offset, fatigue.t, fatigue_filtered)

weights_env=fun.huelle(weights_offset, weights.t, weights_gleich, 3)
fatigue_env=fun.huelle(fatigue_offset, fatigue.t, fatigue_gleich, 3)

#mvc_s,mvc_e,weights_s,weights_e,fatigue_s,fatigue_e= lf3.get_bursts(mvc_filtered,weights_filtered,fatigue_filtered)
mvc_s=[927,4940,8165]
mvc_e=[3201,6977,10880]
weights_s= [1091,6451,12449]
weights_e= [4992,10863,16734]
fatigue_s= [875,8695,16550]
fatigue_e= [6957,14847,22354]

mvc_mean=[]
weights_mean=[]
fatigue_mean=[]

for i in range(3):
   mvc_mean.append(np.mean(mvc_env[mvc_s[i]:mvc_e[i]]))
   weights_mean.append(np.mean(weights_env[weights_s[i]:weights_e[i]]))
   fatigue_mean.append(np.mean(fatigue_env[fatigue_s[i]:fatigue_e[i]]))

print (mvc_mean, weights_mean, fatigue_mean)
real_mvc=np.mean(mvc_mean)
weights_percentage= weights_mean/real_mvc
fatigue_percentage= fatigue_mean/real_mvc

print ('Bei einem Gewicht von 20 % des MVC ergibt siche eine gemessene Muskelaktivierung von '+str(round(weights_percentage[0]*100,2))+' % der maximalen willkürlichen Kontraktion')
print ('Bei einem Gewicht von 50 % des MVC ergibt siche eine gemessene Muskelaktivierung von '+str(round(weights_percentage[1]*100,2))+' % der maximalen willkürlichen Kontraktion')
print ('Bei einem Gewicht von 75 % des MVC ergibt siche eine gemessene Muskelaktivierung von '+str(round(weights_percentage[2]*100,2))+' % der maximalen willkürlichen Kontraktion')

print ('In Experiment 3 ergibt sich bei Duchgang 1 eine gemessene Muskelaktivierung von '+str(round(fatigue_percentage[0]*100,2)) + ' % der maximalen willkürlichen Kontraktion' )
print ('In Experiment 3 ergibt sich bei Duchgang 2 eine gemessene Muskelaktivierung von '+str(round(fatigue_percentage[1]*100,2)) + ' % der maximalen willkürlichen Kontraktion' )
print ('In Experiment 3 ergibt sich bei Duchgang 3 eine gemessene Muskelaktivierung von '+str(round(fatigue_percentage[2]*100,2)) + ' % der maximalen willkürlichen Kontraktion' )

