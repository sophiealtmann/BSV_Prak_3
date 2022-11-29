import numpy as np
from scipy import fftpack
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
import Lab3Functions as lf3

## Offset eliminieren

def eliminateoffset(emg, time):
    nooffset = emg - np.mean(emg)
    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.plot( time, emg)
    ax2.plot(time, nooffset)
    plt.show()
    plt.savefig("No Offset.svg")
    return nooffset

##Filtern zwischen 20 und 450 Hz
#Wert für Wn bei digitalem Filter = Grenzfrequenz durch Hälfte der Abtastfrequenz
# Wn = 20 / (1000/2) bzw. 450 / (1000/2)

def filter(nooffset, time):
    b, a = signal.butter(4, 20/500 , "low", analog=False )
    emg_filtered= signal.filtfilt(b, a , nooffset)

    d, c = signal.butter(4, 450/500 , "high", analog=False )
    emg_filtered= signal.filtfilt(d, c , nooffset)

    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.plot(time, nooffset)
    ax2.plot(time, emg_filtered)
    plt.savefig("filtered.png")
    plt.show()
 
# Gleichrichten des Signals
def gleich():
    emg_gleich = []
    for i in range(len(emg_filtered)):
    if mmemg[i] <= 0:
        emg_gleich.append( abs(mmemg[i])) 
    else:
        emg_gleich.append( mmemg[i])
        
    emgleich = np.array(emg_gleich)
    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.plot(mtime, emg_filtered)
    ax2.plot(mtime, emgleich)
    plt.show()