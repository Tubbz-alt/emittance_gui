import os
import sys
import matplotlib.pyplot as plt

sys.path.append('C:/Users/asihn/Anaconda3/Lib/site-packages')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/lcls_tools/devices/profile_monitor')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/lcls_tools/devices/magnet')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/lcls_tools/image_processing')

from lcls_tools import image_processing as imp
import numpy as np

image = imp.mat_image.MatImage()
image.load_mat_image("ProfMon-example.mat")
print(np.shape(image.image))
image.show_image()
plt.show()
