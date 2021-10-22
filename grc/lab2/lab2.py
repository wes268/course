#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Lab 2
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
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from math import pi
import numpy as np
from gnuradio import qtgui

class lab2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Lab 2")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Lab 2")
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

        self.settings = Qt.QSettings("GNU Radio", "lab2")

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
        self.sps = sps = 8
        self.roll_off = roll_off = 0.5
        self.freqc = freqc = 900
        self.std_dev = std_dev = 0.05
        self.samp_rate = samp_rate = 1000
        self.rrc_filter = rrc_filter = firdes.root_raised_cosine(4, sps, 1, roll_off, 32*sps+1)
        self.phase = phase = 0
        self.lw = lw = 2
        self.gain_ = gain_ = 0.5
        self.freqc_ = freqc_ = freqc
        self.fps = fps = 30
        self.const = const = digital.constellation_calcdist(digital.psk_2()[0], digital.psk_2()[1],
        2, 1).base()
        self.bw = bw = 1
        self.buff_size = buff_size = 32768
        self.bNoise = bNoise = 0
        self.bFilter = bFilter = 0
        self.axis = axis = 2
        self.N = N = 0

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
        self.tab0.addTab(self.tab0_widget_1, 'Eye Diagram')
        self.top_grid_layout.addWidget(self.tab0, 0, 0, 10, 2)
        for r in range(0, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._std_dev_range = Range(0, 1, 0.01, 0.05, 200)
        self._std_dev_win = RangeWidget(self._std_dev_range, self.set_std_dev, 'Noise Std. Dev', "counter_slider", float)
        self.top_grid_layout.addWidget(self._std_dev_win, 11, 0, 1, 1)
        for r in range(11, 12):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._phase_range = Range(-180*2, 180*2, 0.1, 0, 200)
        self._phase_win = RangeWidget(self._phase_range, self.set_phase, 'Phase Offset (Degrees)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._phase_win, 11, 1, 1, 1)
        for r in range(11, 12):
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
        # Create the options list
        self._bNoise_options = (0, 1, )
        # Create the labels list
        self._bNoise_labels = ('Noise Only', 'Signal + Noise', )
        # Create the combo box
        # Create the radio buttons
        self._bNoise_group_box = Qt.QGroupBox('Waveform Select' + ": ")
        self._bNoise_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._bNoise_button_group = variable_chooser_button_group()
        self._bNoise_group_box.setLayout(self._bNoise_box)
        for i, _label in enumerate(self._bNoise_labels):
            radio_button = Qt.QRadioButton(_label)
            self._bNoise_box.addWidget(radio_button)
            self._bNoise_button_group.addButton(radio_button, i)
        self._bNoise_callback = lambda i: Qt.QMetaObject.invokeMethod(self._bNoise_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._bNoise_options.index(i)))
        self._bNoise_callback(self.bNoise)
        self._bNoise_button_group.buttonClicked[int].connect(
            lambda i: self.set_bNoise(self._bNoise_options[i]))
        self.top_grid_layout.addWidget(self._bNoise_group_box, 12, 1, 1, 1)
        for r in range(12, 13):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._bFilter_options = (0, 1, )
        # Create the labels list
        self._bFilter_labels = ('Rectangular', 'Raised Cosine', )
        # Create the combo box
        # Create the radio buttons
        self._bFilter_group_box = Qt.QGroupBox('Pulse Shaping Select' + ": ")
        self._bFilter_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._bFilter_button_group = variable_chooser_button_group()
        self._bFilter_group_box.setLayout(self._bFilter_box)
        for i, _label in enumerate(self._bFilter_labels):
            radio_button = Qt.QRadioButton(_label)
            self._bFilter_box.addWidget(radio_button)
            self._bFilter_button_group.addButton(radio_button, i)
        self._bFilter_callback = lambda i: Qt.QMetaObject.invokeMethod(self._bFilter_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._bFilter_options.index(i)))
        self._bFilter_callback(self.bFilter)
        self._bFilter_button_group.buttonClicked[int].connect(
            lambda i: self.set_bFilter(self._bFilter_options[i]))
        self.top_grid_layout.addWidget(self._bFilter_group_box, 12, 0, 1, 1)
        for r in range(12, 13):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._N_range = Range(0, 7, 1, 0, 200)
        self._N_win = RangeWidget(self._N_range, self.set_N, 'Nth Sample', "counter_slider", float)
        self.top_grid_layout.addWidget(self._N_win, 13, 1, 1, 1)
        for r in range(13, 14):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._roll_off_range = Range(0.01, 0.99, 0.01, 0.5, 200)
        self._roll_off_win = RangeWidget(self._roll_off_range, self.set_roll_off, 'Beta (Roll-Off-Factor)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._roll_off_win, 13, 0, 1, 1)
        for r in range(13, 14):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            2*sps, #size
            1, #samp_rate
            "", #name
            10 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(1/fps)
        self.qtgui_time_sink_x_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "buffer_start")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [lw, lw, lw, lw, lw,
            lw, lw, lw, lw, lw]
        colors = ['blue', 'red', 'yellow', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(10):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab0_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_win, 0, 0, 5, 1)
        for r in range(0, 5):
            self.tab0_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tab0_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
            int(1e5),
            400,
            -axis,
            axis,
            "",
            1
        )

        self.qtgui_histogram_sink_x_0.set_update_time(1/fps)
        self.qtgui_histogram_sink_x_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0.enable_grid(True)
        self.qtgui_histogram_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers= [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab0_grid_layout_0.addWidget(self._qtgui_histogram_sink_x_0_win, 5, 1, 5, 1)
        for r in range(5, 10):
            self.tab0_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tab0_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_RECTANGULAR, #wintype
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
        self.qtgui_freq_sink_x_0_0.set_fft_average(0.05)
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
            firdes.WIN_RECTANGULAR, #wintype
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
        self.qtgui_freq_sink_x_0.set_fft_average(0.05)
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
        self.qtgui_const_sink_x_0.set_y_axis(-axis, axis)
        self.qtgui_const_sink_x_0.set_x_axis(-axis, axis)
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
        self.tab0_grid_layout_0.addWidget(self._qtgui_const_sink_x_0_win, 0, 1, 5, 1)
        for r in range(0, 5):
            self.tab0_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tab0_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0.set_processor_affinity([0])
        self.interp_fir_filter_xxx_1_0 = filter.interp_fir_filter_ccc(sps, (1,1,1,1,1,1,1,1))
        self.interp_fir_filter_xxx_1_0.declare_sample_delay(0)
        self.interp_fir_filter_xxx_1 = filter.interp_fir_filter_ccc(sps, rrc_filter)
        self.interp_fir_filter_xxx_1.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(1, rrc_filter)
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self._freqc__range = Range(70, 6000, .01, freqc, 200)
        self._freqc__win = RangeWidget(self._freqc__range, self.set_freqc_, 'Carrier (MHz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freqc__win, 10, 0, 1, 1)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.digital_chunks_to_symbols_xx_1 = digital.chunks_to_symbols_bc(const.points(), 1)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_gr_complex*1,bFilter,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,N,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(np.exp(1j*2*pi*phase/360))
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_cc(2)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(bNoise)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(gain_ )
        self.blocks_delay_0_2 = blocks.delay(gr.sizeof_float*1, -N+1024)
        self.blocks_delay_0_1 = blocks.delay(gr.sizeof_float*1, sps)
        self.blocks_delay_0_0_1 = blocks.delay(gr.sizeof_float*1, sps)
        self.blocks_delay_0_0_0_1_0 = blocks.delay(gr.sizeof_float*1, sps)
        self.blocks_delay_0_0_0_1 = blocks.delay(gr.sizeof_float*1, sps)
        self.blocks_delay_0_0_0_0_0 = blocks.delay(gr.sizeof_float*1, sps)
        self.blocks_delay_0_0_0_0 = blocks.delay(gr.sizeof_float*1, sps)
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_float*1, sps)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_float*1, sps)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, sps)
        self.blocks_deinterleave_0 = blocks.deinterleave(gr.sizeof_gr_complex*1, 1)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_imag_0 = blocks.complex_to_imag(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2, 8192))), True)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, std_dev*(1.414), 0)
        self.analog_agc_xx_0 = analog.agc_cc(1e-4, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_deinterleave_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_chunks_to_symbols_xx_1, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_imag_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_delay_0_2, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.blocks_deinterleave_0, 4), (self.blocks_selector_0, 4))
        self.connect((self.blocks_deinterleave_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_deinterleave_0, 2), (self.blocks_selector_0, 2))
        self.connect((self.blocks_deinterleave_0, 1), (self.blocks_selector_0, 1))
        self.connect((self.blocks_deinterleave_0, 5), (self.blocks_selector_0, 5))
        self.connect((self.blocks_deinterleave_0, 3), (self.blocks_selector_0, 3))
        self.connect((self.blocks_deinterleave_0, 7), (self.blocks_selector_0, 7))
        self.connect((self.blocks_deinterleave_0, 6), (self.blocks_selector_0, 6))
        self.connect((self.blocks_delay_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.blocks_delay_0_0_0, 0), (self.blocks_delay_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0, 0), (self.qtgui_time_sink_x_0, 3))
        self.connect((self.blocks_delay_0_0_0_0, 0), (self.blocks_delay_0_1, 0))
        self.connect((self.blocks_delay_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 4))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_delay_0_0_0_1_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0, 8))
        self.connect((self.blocks_delay_0_0_0_1, 0), (self.blocks_delay_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_1, 0), (self.qtgui_time_sink_x_0, 7))
        self.connect((self.blocks_delay_0_0_0_1_0, 0), (self.qtgui_time_sink_x_0, 9))
        self.connect((self.blocks_delay_0_0_1, 0), (self.blocks_delay_0_0_0_1, 0))
        self.connect((self.blocks_delay_0_0_1, 0), (self.qtgui_time_sink_x_0, 6))
        self.connect((self.blocks_delay_0_1, 0), (self.blocks_delay_0_0_1, 0))
        self.connect((self.blocks_delay_0_1, 0), (self.qtgui_time_sink_x_0, 5))
        self.connect((self.blocks_delay_0_2, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_delay_0_2, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.qtgui_const_sink_x_0, 1))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_complex_to_imag_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.interp_fir_filter_xxx_1, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.interp_fir_filter_xxx_1_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.interp_fir_filter_xxx_1, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.interp_fir_filter_xxx_1_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lab2")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_filter(firdes.root_raised_cosine(4, self.sps, 1, self.roll_off, 32*self.sps+1))
        self.blocks_delay_0.set_dly(self.sps)
        self.blocks_delay_0_0.set_dly(self.sps)
        self.blocks_delay_0_0_0.set_dly(self.sps)
        self.blocks_delay_0_0_0_0.set_dly(self.sps)
        self.blocks_delay_0_0_0_0_0.set_dly(self.sps)
        self.blocks_delay_0_0_0_1.set_dly(self.sps)
        self.blocks_delay_0_0_0_1_0.set_dly(self.sps)
        self.blocks_delay_0_0_1.set_dly(self.sps)
        self.blocks_delay_0_1.set_dly(self.sps)

    def get_roll_off(self):
        return self.roll_off

    def set_roll_off(self, roll_off):
        self.roll_off = roll_off
        self.set_rrc_filter(firdes.root_raised_cosine(4, self.sps, 1, self.roll_off, 32*self.sps+1))

    def get_freqc(self):
        return self.freqc

    def set_freqc(self, freqc):
        self.freqc = freqc
        self.set_freqc_(self.freqc)

    def get_std_dev(self):
        return self.std_dev

    def set_std_dev(self, std_dev):
        self.std_dev = std_dev
        self.analog_noise_source_x_0.set_amplitude(self.std_dev*(1.414))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate*1e3)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate*1e3)

    def get_rrc_filter(self):
        return self.rrc_filter

    def set_rrc_filter(self, rrc_filter):
        self.rrc_filter = rrc_filter
        self.interp_fir_filter_xxx_0.set_taps(self.rrc_filter)
        self.interp_fir_filter_xxx_1.set_taps(self.rrc_filter)

    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase
        self.blocks_multiply_const_vxx_1.set_k(np.exp(1j*2*pi*self.phase/360))

    def get_lw(self):
        return self.lw

    def set_lw(self, lw):
        self.lw = lw

    def get_gain_(self):
        return self.gain_

    def set_gain_(self, gain_):
        self.gain_ = gain_
        self.blocks_multiply_const_vxx_0.set_k(self.gain_ )

    def get_freqc_(self):
        return self.freqc_

    def set_freqc_(self, freqc_):
        self.freqc_ = freqc_

    def get_fps(self):
        return self.fps

    def set_fps(self, fps):
        self.fps = fps
        self.qtgui_const_sink_x_0.set_update_time(1/self.fps)
        self.qtgui_freq_sink_x_0.set_update_time(1/self.fps)
        self.qtgui_freq_sink_x_0_0.set_update_time(1/self.fps)
        self.qtgui_histogram_sink_x_0.set_update_time(1/self.fps)
        self.qtgui_time_sink_x_0.set_update_time(1/self.fps)

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw

    def get_buff_size(self):
        return self.buff_size

    def set_buff_size(self, buff_size):
        self.buff_size = buff_size

    def get_bNoise(self):
        return self.bNoise

    def set_bNoise(self, bNoise):
        self.bNoise = bNoise
        self._bNoise_callback(self.bNoise)
        self.blocks_multiply_const_vxx_0_0.set_k(self.bNoise)

    def get_bFilter(self):
        return self.bFilter

    def set_bFilter(self, bFilter):
        self.bFilter = bFilter
        self._bFilter_callback(self.bFilter)
        self.blocks_selector_0_0.set_input_index(self.bFilter)

    def get_axis(self):
        return self.axis

    def set_axis(self, axis):
        self.axis = axis
        self.qtgui_histogram_sink_x_0.set_x_axis(-self.axis, self.axis)

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N
        self.blocks_delay_0_2.set_dly(-self.N+1024)
        self.blocks_selector_0.set_input_index(self.N)



def main(top_block_cls=lab2, options=None):

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
