import numpy as np
from scipy import fftpack
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
import Lab3Functions as lf3
import Functions as fun

# Daten importieren
weights,mvc,fatigue=lf3.import_data("\t")

# Offset eliminieren
nooffset= fun.eliminateoffset(mvc.emg, mvc.t)

# Filtern zwischen 20 und 450 Hz
emg_filtered = fun.filter(nooffset, mvc.t)

# Gleichrichten des Signals
em_gleich = fun.gleich(nooffset, mvc.t, emg_filtered)

# Einhüllende bilden
fun.huelle(nooffset, mvc.t, em_gleich, 3)

mvc_offset=fun.eliminateoffset(mvc.emg, mvc.t)
weights_offset=fun.eliminateoffset(weights.emg, weights.t)
fatigue_offset=fun.eliminateoffset(fatigue.emg, fatigue.t)

mvc_filtered=fun.filter(mvc_offset,mvc.t)
weights_filtered=fun.filter(weights_offset,weights.t)
fatigue_filtered=fun.filter(fatigue_offset,fatigue.t)