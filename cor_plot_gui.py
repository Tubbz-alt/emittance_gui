from qtpy import QtWidgets
from pydm import Display

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import sys

sys.path.append('C:/Users/asihn/Anaconda3/Lib/site-packages')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/lcls_tools/devices/profile_monitor')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/lcls_tools/devices/magnet')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/lcls_tools/image_processing')
sys.path.append('C:/Users/asihn/Desktop/SLAC/lcls-tools/lcls_tools/cor_plot')

from cor_plot_mat_scan import CorPlotMatScan as C


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class DemoScreen(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DemoScreen, self).__init__(parent=parent, args=args,
                                         macros=macros)
        self.setup_ui()

    def setup_ui(self):
        self.ui.btn_open_file.clicked.connect(self.handle_open_file)
        self.ui.btn_plot.clicked.connect(self.handle_plot)

        self.plot = MplCanvas(self)
        #self.scatter_plot = MplCanvas(self)
        self.ui.plots_frame.layout().addWidget(self.plot)
        #self.ui.plots_frame.layout().addWidget(self.scatter_plot)

    def ui_filename(self):
        return 'emittance_gui.ui'

    def handle_open_file(self):
        print('Handling open file')
        filter = 'Mat Files (*.mat)'
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                                                      filter=filter)
        fname = fname[0] if isinstance(fname, (list, tuple)) else fname
        self.ui.lbl_current_file.setText(fname)

    def handle_plot(self):
        # clear plots:
        self.plot.axes.cla()

        data = C("C:/Users/asihn/Desktop/SLAC/emittance_gui/CorrelationPlot/CorrelationPlot-SOLN_IN20_121_BCTRL-2020-06-21-091733.mat")

        s = data.samples
        x = data.ctrl_vals

        yarray = []
        yerr = []

        for i in range(0, len(x)):

            yvals = []

            for j in range(0, s):
                yvals.append(((data.beam[i][j][0]['xStat'])[0])[2])

            # calculate average of data and store in array
            meany = np.mean(yvals)
            yarray.append(meany)

            # calculate error of data and store in array
            stdy = np.std(yvals)
            yerr.append(stdy)

        #self.plot.axes.plot(x, yarray)
        self.plot.axes.errorbar(x, yarray, yerr=yerr, label='xStat', ecolor='red', elinewidth=4, linewidth=2, marker='o', markersize=4)
        self.plot.axes.set_title('Correlation Plot')
        self.plot.axes.set_xlabel('Magnet Strength (kG-m)')
        self.plot.axes.set_ylabel('X rms (beam size) (um)')

        # self.plot.axes.legend(loc='upper left')
        self.plot.draw()
