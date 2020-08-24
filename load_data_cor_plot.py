import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append('C:/Users/asihn/Anaconda3/Lib/site-packages')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/lcls_tools/devices/profile_monitor')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/lcls_tools/devices/magnet')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/lcls_tools/image_processing')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/lcls_tools/cor_plot')

from cor_plot_mat_scan import CorPlotMatScan as C

# load data
data = C("C:/Users/asihn/Desktop/SLAC/emittance_gui/CorrelationPlot/CorrelationPlot-SOLN_IN20_121_BCTRL-2020-06-21-091733.mat")

# set the number of samples
s = data.samples

# can use to see the number of data points
#print(data.beam.keys())

# set the x values for plot
x = data.ctrl_vals

# format: data.beam[iteration][sample][fit][beam_name]
# iteration: length of x
# sample: number of samples
# fit: index 0-6 (see types of fit below)
# beam_name": string chosen from types of beam_names below
# types of fit: ['Gaussian', 'Asymmetric', 'Super', 'RMS', 'RMS cut peak', 'RMS cut area', 'RMS floor']
# types of beam_name: profx, xStat, profy, yStat, profu, uStat, stats

yarray = []
yerr = []

for i in range(0, len(x)):

    yvals = []

    for j in range(0, s):
        # store data in array
        yvals.append(((data.beam[i][j][0]['xStat'])[0])[2])

    # calculate average of data and store in array
    meany = np.mean(yvals)
    yarray.append(meany)

    # calculate error of data and store in array
    stdy = np.std(yvals)
    yerr.append(stdy)

# Correlation plot
plt.xlabel('Magnet Strength (kG-m)', fontsize=20)
plt.ylabel('X rms (beam size) (μm)', fontsize=20)
plt.errorbar(x, yarray, yerr=yerr, label='xStat', ecolor='red', elinewidth=4, linewidth=2, marker='o', markersize=4)
plt.title('Correlation Plot', fontsize=30)
plt.legend(loc='upper left')

plt.show()
