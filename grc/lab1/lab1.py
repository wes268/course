#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Lab 1
# Author: wes
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

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from math import pi
import iio
import numpy as np
from gnuradio import qtgui

class lab1(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Lab 1")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Lab 1")
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

        self.settings = Qt.QSettings("GNU Radio", "lab1")

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
        self.freqc = freqc = 900
        self.sps = sps = 8
        self.samp_rate = samp_rate = 1000
        self.phase = phase = 0
        self.mod_M = mod_M = 0
        self.gain_ = gain_ = 0.5
        self.freqc_ = freqc_ = freqc
        self.fps = fps = 30
        self.foffset = foffset = 0
        self.bw = bw = 1
        self.buff_size = buff_size = 32768
        self.analog_gain = analog_gain = 32

        ##################################################
        # Blocks
        ##################################################
        self.tab0 = Qt.QTabWidget()
        self.tab0_widget_0 = Qt.QWidget()
        self.tab0_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab0_widget_0)
        self.tab0_grid_layout_0 = Qt.QGridLayout()
        self.tab0_layout_0.addLayout(self.tab0_grid_layout_0)
        self.tab0.addTab(self.tab0_widget_0, 'Spectrum/Constellation')
        self.tab0_widget_1 = Qt.QWidget()
        self.tab0_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab0_widget_1)
        self.tab0_grid_layout_1 = Qt.QGridLayout()
        self.tab0_layout_1.addLayout(self.tab0_grid_layout_1)
        self.tab0.addTab(self.tab0_widget_1, 'Time-Series')
        self.top_grid_layout.addWidget(self.tab0, 0, 0, 10, 2)
        for r in range(0, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._phase_range = Range(-180*2, 180*2, 0.1, 0, 200)
        self._phase_win = RangeWidget(self._phase_range, self.set_phase, 'Phase Offset (Degrees)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._phase_win, 11, 1, 1, 1)
        for r in range(11, 12):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._mod_M_options = (0, 1, )
        # Create the labels list
        self._mod_M_labels = ('BPSK', 'QPSK', )
        # Create the combo box
        # Create the radio buttons
        self._mod_M_group_box = Qt.QGroupBox('Modulation Select' + ": ")
        self._mod_M_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._mod_M_button_group = variable_chooser_button_group()
        self._mod_M_group_box.setLayout(self._mod_M_box)
        for i, _label in enumerate(self._mod_M_labels):
            radio_button = Qt.QRadioButton(_label)
            self._mod_M_box.addWidget(radio_button)
            self._mod_M_button_group.addButton(radio_button, i)
        self._mod_M_callback = lambda i: Qt.QMetaObject.invokeMethod(self._mod_M_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._mod_M_options.index(i)))
        self._mod_M_callback(self.mod_M)
        self._mod_M_button_group.buttonClicked[int].connect(
            lambda i: self.set_mod_M(self._mod_M_options[i]))
        self.top_grid_layout.addWidget(self._mod_M_group_box, 12, 1, 1, 1)
        for r in range(12, 13):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain__range = Range(0.1, 1, 0.01, 0.5, 200)
        self._gain__win = RangeWidget(self._gain__range, self.set_gain_, 'Gain (Amp)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain__win, 10, 1, 1, 1)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freqc__range = Range(70, 6000, .01, freqc, 200)
        self._freqc__win = RangeWidget(self._freqc__range, self.set_freqc_, 'Carrier (MHz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freqc__win, 10, 0, 1, 1)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._foffset_range = Range(-10, 10, 1, 0, 10)
        self._foffset_win = RangeWidget(self._foffset_range, self.set_foffset, 'Frequency Offset (Hz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._foffset_win, 12, 0, 1, 1)
        for r in range(12, 13):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._analog_gain_range = Range(0, 64, 1, 32, 200)
        self._analog_gain_win = RangeWidget(self._analog_gain_range, self.set_analog_gain, 'Gain (Analog)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._analog_gain_win, 11, 0, 1, 1)
        for r in range(11, 12):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            131072, #size
            samp_rate*1000, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(1/fps)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab0_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_win, 0, 0, 10, 2)
        for r in range(0, 10):
            self.tab0_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 2):
            self.tab0_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate*1e3, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(1/fps)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)



        labels = ['Magnitude', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.tab0_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_0_win, 0, 0, 5, 1)
        for r in range(0, 5):
            self.tab0_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tab0_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0.set_processor_affinity([0])
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate*1e3, #bw
            "", #name
            2
        )
        self.qtgui_freq_sink_x_0.set_update_time(1/fps)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['In-Phase', 'Quadrature', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab0_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 5, 0, 5, 1)
        for r in range(5, 10):
            self.tab0_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tab0_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0.set_processor_affinity([0])
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            2 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(1/fps)
        self.qtgui_const_sink_x_0.set_y_axis(-3, 3)
        self.qtgui_const_sink_x_0.set_x_axis(-3, 3)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 1, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, -1, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 0.5, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab0_grid_layout_0.addWidget(self._qtgui_const_sink_x_0_win, 0, 1, 10, 1)
        for r in range(0, 10):
            self.tab0_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tab0_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0.set_processor_affinity([0])
        self.iio_pluto_source_0 = iio.pluto_source('', int(freqc_*1e6), int(samp_rate*1000), 20000000, buff_size, True, True, True, 'manual', analog_gain, '', True)
        self.iio_pluto_sink_0 = iio.pluto_sink('', int(freqc_*1e6)+foffset, int(samp_rate*1000), 20000000, buff_size, False, 10.0, '', True)
        self.digital_psk_mod_0_0 = digital.psk.psk_mod(
            constellation_points=4,
            mod_code="gray",
            differential=True,
            samples_per_symbol=sps,
            excess_bw=1,
            verbose=False,
            log=False)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(np.exp(1j*2*pi*phase/360))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(mod_M)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(gain_  * np.exp(1j * pi / 4))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_real_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_imag_1 = blocks.complex_to_imag(1)
        self.blocks_complex_to_imag_0 = blocks.complex_to_imag(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 4, 8192))), True)
        self.analog_agc_xx_0 = analog.agc_cc(1e-4,  ( 1.0 + mod_M), 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_complex_to_imag_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.qtgui_const_sink_x_0, 1))
        self.connect((self.analog_agc_xx_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_psk_mod_0_0, 0))
        self.connect((self.blocks_complex_to_imag_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.blocks_complex_to_imag_1, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_imag_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_real_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.digital_psk_mod_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.blocks_multiply_const_vxx_1, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lab1")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_freqc(self):
        return self.freqc

    def set_freqc(self, freqc):
        self.freqc = freqc
        self.set_freqc_(self.freqc)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.iio_pluto_sink_0.set_params(int(self.freqc_*1e6)+self.foffset, int(self.samp_rate*1000), 20000000, 10.0, '', True)
        self.iio_pluto_source_0.set_params(int(self.freqc_*1e6), int(self.samp_rate*1000), 20000000, True, True, True, 'manual', self.analog_gain, '', True)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate*1e3)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate*1e3)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate*1000)

    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase
        self.blocks_multiply_const_vxx_1.set_k(np.exp(1j*2*pi*self.phase/360))

    def get_mod_M(self):
        return self.mod_M

    def set_mod_M(self, mod_M):
        self.mod_M = mod_M
        self._mod_M_callback(self.mod_M)
        self.analog_agc_xx_0.set_reference( ( 1.0 + self.mod_M))
        self.blocks_multiply_const_vxx_0_0.set_k(self.mod_M)

    def get_gain_(self):
        return self.gain_

    def set_gain_(self, gain_):
        self.gain_ = gain_
        self.blocks_multiply_const_vxx_0.set_k(self.gain_  * np.exp(1j * pi / 4))

    def get_freqc_(self):
        return self.freqc_

    def set_freqc_(self, freqc_):
        self.freqc_ = freqc_
        self.iio_pluto_sink_0.set_params(int(self.freqc_*1e6)+self.foffset, int(self.samp_rate*1000), 20000000, 10.0, '', True)
        self.iio_pluto_source_0.set_params(int(self.freqc_*1e6), int(self.samp_rate*1000), 20000000, True, True, True, 'manual', self.analog_gain, '', True)

    def get_fps(self):
        return self.fps

    def set_fps(self, fps):
        self.fps = fps
        self.qtgui_const_sink_x_0.set_update_time(1/self.fps)
        self.qtgui_freq_sink_x_0.set_update_time(1/self.fps)
        self.qtgui_freq_sink_x_0_0.set_update_time(1/self.fps)
        self.qtgui_time_sink_x_0.set_update_time(1/self.fps)

    def get_foffset(self):
        return self.foffset

    def set_foffset(self, foffset):
        self.foffset = foffset
        self.iio_pluto_sink_0.set_params(int(self.freqc_*1e6)+self.foffset, int(self.samp_rate*1000), 20000000, 10.0, '', True)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw

    def get_buff_size(self):
        return self.buff_size

    def set_buff_size(self, buff_size):
        self.buff_size = buff_size

    def get_analog_gain(self):
        return self.analog_gain

    def set_analog_gain(self, analog_gain):
        self.analog_gain = analog_gain
        self.iio_pluto_source_0.set_params(int(self.freqc_*1e6), int(self.samp_rate*1000), 20000000, True, True, True, 'manual', self.analog_gain, '', True)



def main(top_block_cls=lab1, options=None):

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
