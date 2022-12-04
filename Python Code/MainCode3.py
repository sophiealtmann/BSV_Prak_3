import numpy as np
from scipy import fftpack
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
import Lab3Functions as lf3
import Functions as fun
import csv

# Zur Erstellung von Plots müssen in Functions die jeweiligen pyplot funktionen entkommentiert werden. 
# Zur Erleichterung der Weiterverarbeitung wurden diese auskommentiert. 
# Selbiges gilt für die Erstellung von Plots in dieser Datei  

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

# Um bei einer konsistenten Weiterverarbeitung zu bleiben, wurden die Daten wie oben 
# mit der get_bursts Funktion einmal aufgenommen und im folgenden als Variablen abgespeichert. 

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

weights_kg=[2.5,5,7.5]

# mvc_probanden=[['Proband/in','MVC in Nm'],                         auch hier wurde Funktion nur einmal pro Proband durchgeführt und dann auskommentiert
#         ['Bleckenwegner',42.27],                                   um bei den Daten konsistent zu bleiben. 
#         ['Aichinger',44.23],
#         ['Altmann',42.56]]
# with open('./Python Code/Plots/mvc_probanden.csv','w') as file: 
#     writer=csv.writer(file)
#     for row in mvc_probanden:
#         writer.writerow(row)
#     file.close()


# plt.bar(weights_kg,weights_percentage*100)
# plt.xlabel("Weight (kg)")
# plt.ylabel("% of MVC")
# plt.xticks(weights_kg)
# plt.savefig('./Python Code/Plots/weights_mvc.svg')
# plt.show()

burst1_start1=fatigue.t[fatigue_s[0]]+1000
burst1_end1= burst1_start1+500
burst1_start2= burst1_end1+7500
burst1_end2= burst1_start2+500
burst1_start3=fatigue.t[fatigue_e[0]]-1500
burst1_end3= burst1_start3+500

burst2_start1=fatigue.t[fatigue_s[1]]+1000
burst2_end1= burst2_start1+500
burst2_start2= burst2_end1+7500
burst2_end2= burst2_start2+500
burst2_start3=fatigue.t[fatigue_e[1]]-1500
burst2_end3= burst2_start3+500

burst3_start1=fatigue.t[fatigue_s[2]]+1000
burst3_end1= burst3_start1+500
burst3_start2= burst3_end1+7500
burst3_end2= burst3_start2+500
burst3_start3=fatigue.t[fatigue_e[2]]-1500
burst3_end3= burst3_start3+500

burst1_index_s1=np.argmin(np.abs(fatigue.t - burst1_start1))
burst1_index_e1=np.argmin(np.abs(fatigue.t - burst1_end1))
burst1_index_s2=np.argmin(np.abs(fatigue.t - burst1_start2))
burst1_index_e2=np.argmin(np.abs(fatigue.t - burst1_end2))
burst1_index_s3=np.argmin(np.abs(fatigue.t - burst1_start3))
burst1_index_e3=np.argmin(np.abs(fatigue.t - burst1_end3))

burst2_index_s1=np.argmin(np.abs(fatigue.t - burst2_start1))
burst2_index_e1=np.argmin(np.abs(fatigue.t - burst2_end1))
burst2_index_s2=np.argmin(np.abs(fatigue.t - burst2_start2))
burst2_index_e2=np.argmin(np.abs(fatigue.t - burst2_end2))
burst2_index_s3=np.argmin(np.abs(fatigue.t - burst2_start3))
burst2_index_e3=np.argmin(np.abs(fatigue.t - burst2_end3))

burst3_index_s1=np.argmin(np.abs(fatigue.t - burst3_start1))
burst3_index_e1=np.argmin(np.abs(fatigue.t - burst3_end1))
burst3_index_s2=np.argmin(np.abs(fatigue.t - burst3_start2))
burst3_index_e2=np.argmin(np.abs(fatigue.t - burst3_end2))
burst3_index_s3=np.argmin(np.abs(fatigue.t - burst3_start3))
burst3_index_e3=np.argmin(np.abs(fatigue.t - burst3_end3))

b1start_isolated= fatigue_filtered[burst1_index_s1:burst1_index_e1]
b1mid_isolated= fatigue_filtered[burst1_index_s2:burst1_index_e2]
b1end_isolated= fatigue_filtered[burst1_index_s3:burst1_index_e3]

b2start_isolated= fatigue_filtered[burst2_index_s1:burst2_index_e1]
b2mid_isolated= fatigue_filtered[burst2_index_s2:burst2_index_e2]
b2end_isolated= fatigue_filtered[burst2_index_s3:burst2_index_e3]

b3start_isolated= fatigue_filtered[burst3_index_s1:burst3_index_e1]
b3mid_isolated= fatigue_filtered[burst3_index_s2:burst3_index_e2]
b3end_isolated= fatigue_filtered[burst3_index_s3:burst3_index_e3]

b1start_power,b1start_freq=lf3.get_power(b1start_isolated,1000)
b1mid_power,b1mid_freq=lf3.get_power(b1mid_isolated,1000)
b1end_power,b1end_freq=lf3.get_power(b1end_isolated,1000)

b2start_power,b2start_freq=lf3.get_power(b2start_isolated,1000)
b2mid_power,b2mid_freq=lf3.get_power(b2mid_isolated,1000)
b2end_power,b2end_freq=lf3.get_power(b2end_isolated,1000)

b3start_power,b3start_freq=lf3.get_power(b3start_isolated,1000)
b3mid_power,b3mid_freq=lf3.get_power(b3mid_isolated,1000)
b3end_power,b3end_freq=lf3.get_power(b3end_isolated,1000)

b1start_pwrfilt=fun.freqfilt(b1start_power)
b1mid_pwrfilt=fun.freqfilt(b1mid_power)
b1end_pwrfilt=fun.freqfilt(b1end_power)

b2start_pwrfilt=fun.freqfilt(b2start_power)
b2mid_pwrfilt=fun.freqfilt(b2mid_power)
b2end_pwrfilt=fun.freqfilt(b2end_power)

b3start_pwrfilt=fun.freqfilt(b3start_power)
b3mid_pwrfilt=fun.freqfilt(b3mid_power)
b3end_pwrfilt=fun.freqfilt(b3end_power)

b1start_median=fun.getmedian(b1start_power,b1start_freq)
b1mid_median=fun.getmedian(b1mid_power,b1mid_freq)
b1end_median=fun.getmedian(b1end_power,b1end_freq)

b2start_median=fun.getmedian(b2start_power,b2start_freq)
b2mid_median=fun.getmedian(b2mid_power,b2mid_freq)
b2end_median=fun.getmedian(b2end_power,b2end_freq)

b3start_median=fun.getmedian(b3start_power,b3start_freq)
b3mid_median=fun.getmedian(b3mid_power,b3mid_freq)
b3end_median=fun.getmedian(b3end_power,b3end_freq)

# Plots der Leistungsspektren

# plt.plot(b1start_freq,b1start_power/10,label='Unfiltered Power')
# plt.plot(b1start_freq,b1start_pwrfilt/10,color='red',label='Filtered Power')
# plt.axvline(x=b1start_median,color='green',label='Median')
# plt.xlabel('Frequency(Hz)')
# plt.ylabel('Power(dB)')
# plt.legend(loc="best",frameon=True)
# plt.show()

# plt.plot(b1mid_freq,b1mid_power/10,label='Unfiltered Power')
# plt.plot(b1mid_freq,b1mid_pwrfilt/10,color='red',label='Filtered Power')
# plt.axvline(x=b1mid_median,color='green',label='Median')
# plt.xlabel('Frequency(Hz)')
# plt.ylabel('Power(dB)')
# plt.legend(loc="best",frameon=True)
# plt.show()

# plt.plot(b1end_freq,b1end_power/10,label='Unfiltered Power')
# plt.plot(b1end_freq,b1end_pwrfilt/10,color='red',label='Filtered Power')
# plt.axvline(x=b1end_median,color='green',label='Median')
# plt.xlabel('Frequency(Hz)')
# plt.ylabel('Power(dB)')
# plt.legend(loc="best",frameon=True)
# plt.show()

# plt.plot(b2start_freq,b2start_power/10,label='Unfiltered Power')
# plt.plot(b2start_freq,b2start_pwrfilt/10,color='red',label='Filtered Power')
# plt.axvline(x=b2start_median,color='green',label='Median')
# plt.xlabel('Frequency(Hz)')
# plt.ylabel('Power(dB)')
# plt.legend(loc="best",frameon=True)
# plt.savefig('./Python Code/Plots/leistungsspektrum.svg')
# plt.show()

# plt.plot(b2mid_freq,b2mid_power/10,label='Unfiltered Power')
# plt.plot(b2mid_freq,b2mid_pwrfilt/10,color='red',label='Filtered Power')
# plt.axvline(x=b2mid_median,color='green',label='Median')
# plt.xlabel('Frequency(Hz)')
# plt.ylabel('Power(dB)')
# plt.legend(loc="best",frameon=True)
# plt.show()

# plt.plot(b2end_freq,b2end_power/10,label='Unfiltered Power')
# plt.plot(b2end_freq,b2end_pwrfilt/10,color='red',label='Filtered Power')
# plt.axvline(x=b2end_median,color='green',label='Median')
# plt.xlabel('Frequency(Hz)')
# plt.ylabel('Power(dB)')
# plt.legend(loc="best",frameon=True)
# plt.show()

# plt.plot(b3start_freq,b3start_power/10,label='Unfiltered Power')
# plt.plot(b3start_freq,b3start_pwrfilt/10,color='red',label='Filtered Power')
# plt.axvline(x=b3start_median,color='green',label='Median')
# plt.xlabel('Frequency(Hz)')
# plt.ylabel('Power(dB)')
# plt.legend(loc="best",frameon=True)
# plt.show()

# plt.plot(b3mid_freq,b3mid_power/10,label='Unfiltered Power')
# plt.plot(b3mid_freq,b3mid_pwrfilt/10,color='red',label='Filtered Power')
# plt.axvline(x=b3mid_median,color='green',label='Median')
# plt.xlabel('Frequency(Hz)')
# plt.ylabel('Power(dB)')
# plt.legend(loc="best",frameon=True)
# plt.show()

# plt.plot(b3end_freq,b3end_power/10,label='Unfiltered Power')
# plt.plot(b3end_freq,b3end_pwrfilt/10,color='red',label='Filtered Power')
# plt.axvline(x=b3end_median,color='green',label='Median')
# plt.xlabel('Frequency(Hz)')
# plt.ylabel('Power(dB)')
# plt.legend(loc="best",frameon=True)
# plt.show()



median_time=['start','middle','end']
median_ex1=[b1start_median,b1mid_median,b1end_median]
median_ex2=[b2start_median,b2mid_median,b2end_median]
median_ex3=[b3start_median,b3mid_median,b3end_median]

# Plot des Medianverlaufes 

# plt.scatter(median_time,median_ex1,marker='*')
# plt.plot(median_time,median_ex1,label="1st cycle")
# plt.scatter(median_time,median_ex2,marker='*')
# plt.plot(median_time,median_ex2,label="2nd cycle")
# plt.scatter(median_time,median_ex3,marker='*')
# plt.plot(median_time,median_ex3,label="3rd cycle")
# plt.xlabel('Time within experiment')
# plt.ylabel('Median Frequency (Hz)')
# plt.legend(loc='best',frameon=True)
# plt.savefig('./Python Code/Plots/median_freq.svg')
# plt.show()