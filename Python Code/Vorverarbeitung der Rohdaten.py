import numpy as np
from scipy import fftpack
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
import Lab3Functions as lf3

## Importieren der Daten
weights,mvc,fatigue=lf3.import_data(";")

wemg = weights.emg
wtime = weights.t

memg = mvc.emg
mtime = mvc.t

femg = fatigue.emg
ftime = fatigue.t

## Offset eliminieren
mmemg = memg - np.mean(memg)
fig, (ax1, ax2) = plt.subplots(1,2)
ax1.plot( mtime, memg)
ax2.plot(mtime, mmemg)
plt.show()


## Filtern zwischen 20 und 450 Hz
# Wert für Wn bei digitalem Filter = Grenzfrequenz durch Hälfte der Abtastfrequenz
# Wn = 20 / (1000/2) bzw. 450 / (1000/2)

b, a = signal.butter(4, 20/500 , "low", analog=False )
emg_filtered= signal.filtfilt(b, a , mmemg)

d, c = signal.butter(4, 450/500 , "high", analog=False )
emg_filtered= signal.filtfilt(d, c , mmemg)

fig, (ax1, ax2) = plt.subplots(1,2)
ax1.plot(mtime, mmemg)
ax2.plot(mtime, emg_filtered)
plt.show()
#plt.savefig("filtered.png")

## Signal gleichrichten
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


## Einhüllende mit Grenzfrequenz von 3 Hz bilden
b, a = signal.butter(4, 4/500 , "low", analog=False )
emg_gfiltered= signal.filtfilt(b, a , mmemg)

fig, (ax1, ax2) = plt.subplots(2,1)
ax1.plot(mtime, emg_gfiltered)
ax2.plot(mtime, emgleich)
plt.show()