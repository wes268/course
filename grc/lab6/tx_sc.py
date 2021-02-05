#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: TX Single-Carrier
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.digital.utils import tagged_streams
from gnuradio.qtgui import Range, RangeWidget
from pulse_shape_hier import pulse_shape_hier  # grc-generated hier_block
import iio
import numpy as np
from gnuradio import qtgui

class tx_sc(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "TX Single-Carrier")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("TX Single-Carrier")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "tx_sc")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.tx_amp = tx_amp = 0.2
        self.signal_select = signal_select = 0
        self.samp_rate = samp_rate = 4e6
        self.rx_gain = rx_gain = 30
        self.freqc = freqc = 900e6
        self.beta = beta = 0.5

        ##################################################
        # Blocks
        ##################################################
        self._tx_amp_range = Range(0, 0.5, .001, 0.2, 200)
        self._tx_amp_win = RangeWidget(self._tx_amp_range, self.set_tx_amp, 'TX Amplitude', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_amp_win, 1, 0, 1, 8)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._signal_select_options = (0, 1, 2, )
        # Create the labels list
        self._signal_select_labels = ('Rectangular', 'Raised Cosine', 'Root-Raised Cosine', )
        # Create the combo box
        self._signal_select_tool_bar = Qt.QToolBar(self)
        self._signal_select_tool_bar.addWidget(Qt.QLabel('Signal Select' + ": "))
        self._signal_select_combo_box = Qt.QComboBox()
        self._signal_select_tool_bar.addWidget(self._signal_select_combo_box)
        for _label in self._signal_select_labels: self._signal_select_combo_box.addItem(_label)
        self._signal_select_callback = lambda i: Qt.QMetaObject.invokeMethod(self._signal_select_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._signal_select_options.index(i)))
        self._signal_select_callback(self.signal_select)
        self._signal_select_combo_box.currentIndexChanged.connect(
            lambda i: self.set_signal_select(self._signal_select_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._signal_select_tool_bar, 11, 0, 1, 8)
        for r in range(11, 12):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_gain_range = Range(0, 64, 1, 30, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'RX Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_gain_win, 0, 0, 1, 8)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._beta_range = Range(0.01, 0.99, 0.01, 0.5, 200)
        self._beta_win = RangeWidget(self._beta_range, self.set_beta, 'Beta (Excess BW)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._beta_win, 10, 0, 1, 8)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate/2, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-120, -20)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2, 0, 8, 8)
        for r in range(2, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.pulse_shape_hier_0 = pulse_shape_hier(
            bFilter=signal_select,
            rect_taps=(1,1,1,1),
            roll_off=beta,
            sps=4,
        )
        self.iio_pluto_source_0 = iio.pluto_source('usb:1.4.5', int(freqc), int(samp_rate/2), 20000000, 32768, True, True, True, 'manual', rx_gain, '', True)
        self.iio_pluto_sink_0 = iio.pluto_sink('usb:1.3.5', int(freqc), int(samp_rate), 20000000, 32768, False, 10.0, '', True)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((-1-1j,-1+1j,1-1j,1+1j), 1)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, 2, "", False, gr.GR_LSB_FIRST)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(tx_amp)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 1000))), True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.pulse_shape_hier_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.pulse_shape_hier_0, 0), (self.blocks_multiply_const_vxx_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "tx_sc")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_amp(self):
        return self.tx_amp

    def set_tx_amp(self, tx_amp):
        self.tx_amp = tx_amp
        self.blocks_multiply_const_vxx_0.set_k(self.tx_amp)

    def get_signal_select(self):
        return self.signal_select

    def set_signal_select(self, signal_select):
        self.signal_select = signal_select
        self._signal_select_callback(self.signal_select)
        self.pulse_shape_hier_0.set_bFilter(self.signal_select)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.iio_pluto_sink_0.set_params(int(self.freqc), int(self.samp_rate), 20000000, 10.0, '', True)
        self.iio_pluto_source_0.set_params(int(self.freqc), int(self.samp_rate/2), 20000000, True, True, True, 'manual', self.rx_gain, '', True)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate/2)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.iio_pluto_source_0.set_params(int(self.freqc), int(self.samp_rate/2), 20000000, True, True, True, 'manual', self.rx_gain, '', True)

    def get_freqc(self):
        return self.freqc

    def set_freqc(self, freqc):
        self.freqc = freqc
        self.iio_pluto_sink_0.set_params(int(self.freqc), int(self.samp_rate), 20000000, 10.0, '', True)
        self.iio_pluto_source_0.set_params(int(self.freqc), int(self.samp_rate/2), 20000000, True, True, True, 'manual', self.rx_gain, '', True)

    def get_beta(self):
        return self.beta

    def set_beta(self, beta):
        self.beta = beta
        self.pulse_shape_hier_0.set_roll_off(self.beta)



def main(top_block_cls=tx_sc, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
