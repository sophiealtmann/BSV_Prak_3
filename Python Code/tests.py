import numpy as np
import scipy
from scipy import fftpack
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
import Lab3Functions as lf3
import Functions as fun

weights,mvc,fatigue=lf3.import_data(";")

mvc_offset=fun.eliminateoffset(mvc.emg, mvc.t)
weights_offset=fun.eliminateoffset(weights.emg, weights.t)
fatigue_offset=fun.eliminateoffset(fatigue.emg, fatigue.t)

mvc_filtered=fun.filter(mvc_offset,mvc.t)
weights_filtered=fun.filter(weights_offset,weights.t)
fatigue_filtered=fun.filter(fatigue_offset,fatigue.t)

mvc_gleich = fun.gleich(mvc_offset, mvc.t, mvc_filtered)
weights_gleich=fun.gleich(weights_offset, weights.t, weights_filtered)
fatigue_gleich=fun.gleich(fatigue_offset, fatigue.t, fatigue_filtered)

mvc_env=fun.huelle(mvc_offset, mvc.t, mvc_gleich, 3)
weights_env=fun.huelle(weights_offset, weights.t, weights_gleich, 3)
fatigue_env=fun.huelle(fatigue_offset, fatigue.t, fatigue_gleich, 3)

#mvc_s,mvc_e,weights_s,weights_e,fatigue_s,fatigue_e= lf3.get_bursts(mvc_filtered,weights_filtered,fatigue_filtered)

mvc_s=[927,4940,8165]
mvc_e=[3201,6977,10880]
weights_s= [1091,6451,12449]
weights_e= [4992,10863,16734]
fatigue_s= [875,8695,16550]
fatigue_e= [6957,14847,22354]



index_s1=np.argmin(np.abs(fatigue.t - 2500))
index_e1=np.argmin(np.abs(fatigue.t - 3000))
index_s2=np.argmin(np.abs(fatigue.t - 9200))
index_e2=np.argmin(np.abs(fatigue.t - 9700))
index_s3=np.argmin(np.abs(fatigue.t - 15500))
index_e3=np.argmin(np.abs(fatigue.t - 16000))


start_isolated= fatigue_filtered[index_s1:index_e1]
middle_isolated= fatigue_filtered[index_s2:index_e2]
end_isolated= fatigue_filtered[index_s3:index_e3]


power,frequencies=lf3.get_power(middle_isolated,1000)

b, a = signal.butter(4, 40/500 , "low", analog=False )
power_filtered=signal.filtfilt(b,a,power)
area_freq= scipy.integrate.cumtrapz(power,frequencies, initial=0)
total_power=area_freq[-1]
median_freq= frequencies[np.where(area_freq >= total_power/2)[0][0]]
plt.plot(frequencies,power)
plt.plot(frequencies,power_filtered,color='red')
plt.axvline(x=median_freq)
plt.show()