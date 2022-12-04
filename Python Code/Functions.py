import numpy as np
import scipy
from scipy import fftpack
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
import Lab3Functions as lf3

## Offset eliminieren
def eliminateoffset(emg, time):
    nooffset = emg - np.mean(emg)
    #fig, (ax1, ax2) = plt.subplots(1,2)
    #ax1.plot( time, emg)
    #ax2.plot(time, nooffset)
    #plt.show()
    #plt.savefig("No Offset.svg")

    return nooffset

##Filtern zwischen 20 und 450 Hz
#Wert für Wn bei digitalem Filter = Grenzfrequenz durch Hälfte der Abtastfrequenz
# Wn = 20 / (1000/2) bzw. 450 / (1000/2)

def filter(nooffset, time):
    b, a = signal.butter(4, 20/500 , "high", analog=False)
    emg_filthigh= signal.filtfilt(b, a , nooffset)

    d, c = signal.butter(4, 450/500 , "low", analog=False)
    emg_filtered= signal.filtfilt(d, c , emg_filthigh)

    #fig, (ax1, ax2) = plt.subplots(1,2)
    #ax1.plot(time, nooffset)
    #ax2.plot(time, emg_filtered)
    #plt.savefig("filtered.svg")
    #plt.show()

    return emg_filtered
 
# Gleichrichten des Signals
def gleich(nooffset, time, emg_filtered):
    emg_gleich = []
    for i in range(len(emg_filtered)):
        if nooffset[i] <= 0:
            emg_gleich.append(abs(nooffset[i])) 
        else:
            emg_gleich.append(nooffset[i])
        
    emgleich = np.array(emg_gleich)
    #fig, (ax1, ax2) = plt.subplots(1,2)
    #ax1.plot(time, emg_filtered)
    #ax2.plot(time, emgleich)
    #plt.show()
    #plt.savefig("Gleichgerichtetes Signal.svg")
    return emgleich

# Einhüllende bilden
def huelle(nooffset, time, emgleich, grenzfrequenz):
    b, a = signal.butter(4, grenzfrequenz/500 , "low", analog=False )
    emg_gfiltered= signal.filtfilt(b, a , emgleich)

    #fig, (ax1, ax2) = plt.subplots(2,1)
    #ax1.plot(time, emg_gfiltered)
    #ax2.plot(time, emgleich)
    #plt.show()
    #plt.savefig("Einhüllende.svg")
    return emg_gfiltered

# Filter für das Frequenzspektrum
def freqfilt(power):
    b, a = signal.butter(4, 40/500 , "low", analog=False )
    power_filtered= signal.filtfilt(b, a , power)
    return power_filtered

# Berechnung des Medians
def getmedian(power,frequencies):
    area_freq= scipy.integrate.cumtrapz(power,frequencies, initial=0)
    total_power=area_freq[-1]
    median_freq= frequencies[np.where(area_freq >= total_power/2)[0][0]]
    return median_freq