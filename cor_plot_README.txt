load_data_cor_plot.py

Uses cor_plot tools from lcls-tools.
Loads data and plots a correlation plot from the data.
Error bars indicate the deviance from the mean at each x value.
x values (magnet strength) are found using the tool ctrl_vals.
At each x value, some number of iterations will be taken. 

A specific fit and beam name can be chosen from the following lists:
FIT = ['Gaussian', 'Asymmetric', 'Super', 'RMS', 'RMS cut peak', 'RMS cut area', 'RMS floor']
beam_names: profx, xStat, profy, yStat, profu, uStat, stats

In each iteration, some number of samples are taken.
The mean of the samples in each iteration is taken and appended to a new array.
This new array is used for the y values (beam size).
The x array is plotted against the y array, along with error bars.
