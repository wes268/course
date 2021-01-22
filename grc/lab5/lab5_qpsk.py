#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: QPSK and Gray Coding
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
from gnuradio import qtgui
import sip
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import math
import wes
from gnuradio import qtgui

class lab5_qpsk(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "QPSK and Gray Coding")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("QPSK and Gray Coding")
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

        self.settings = Qt.QSettings("GNU Radio", "lab5_qpsk")

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
        self.reset_ber = reset_ber = 0
        self.frame_size = frame_size = 4096
        self.eb_no_db = eb_no_db = 10
        self.const_non_gray = const_non_gray = digital.constellation_calcdist([1+0j,0+1j,-1+0j,0-1j], digital.psk_4()[1],
        2, 1).base()
        self.const_gray = const_gray = digital.constellation_calcdist(digital.psk_4()[0], digital.psk_4()[1],
        2, 1).base()

        ##################################################
        # Blocks
        ##################################################
        _reset_ber_push_button = Qt.QPushButton('Reset BER')
        _reset_ber_push_button = Qt.QPushButton('Reset BER')
        self._reset_ber_choices = {'Pressed': 1, 'Released': 0}
        _reset_ber_push_button.pressed.connect(lambda: self.set_reset_ber(self._reset_ber_choices['Pressed']))
        _reset_ber_push_button.released.connect(lambda: self.set_reset_ber(self._reset_ber_choices['Released']))
        self.top_grid_layout.addWidget(_reset_ber_push_button)
        self._eb_no_db_range = Range(0, 20, 0.5, 10, 200)
        self._eb_no_db_win = RangeWidget(self._eb_no_db_range, self.set_eb_no_db, 'Eb/No (dB)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._eb_no_db_win)
        self.wes_ber_0_0 = wes.ber(2, reset_ber)
        self.wes_ber_0 = wes.ber(2, reset_ber)
        self.qtgui_number_sink_0_0_0_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            2
        )
        self.qtgui_number_sink_0_0_0_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0_0_0_0.set_title("Gray Coded")

        labels = ['BER', '# Errors', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(2):
            self.qtgui_number_sink_0_0_0_0_0.set_min(i, -1)
            self.qtgui_number_sink_0_0_0_0_0.set_max(i, 1)
            self.qtgui_number_sink_0_0_0_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0_0_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0_0_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0_0_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0_0_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0_0_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_0_0_0_0_win)
        self.qtgui_number_sink_0_0_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            2
        )
        self.qtgui_number_sink_0_0_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0_0_0.set_title("Non-Gray Coded")

        labels = ['BER', '# Errors', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(2):
            self.qtgui_number_sink_0_0_0_0.set_min(i, -1)
            self.qtgui_number_sink_0_0_0_0.set_max(i, 1)
            self.qtgui_number_sink_0_0_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_0_0_0_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
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
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(const_gray)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(const_non_gray)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(const_gray.points(), 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(const_non_gray.points(), 1)
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 4, frame_size))), True)
        self.analog_random_source_x_0.set_min_output_buffer(4096)
        self.analog_random_source_x_0.set_max_output_buffer(4096)
        self.analog_noise_source_x_0_0 = analog.noise_source_c(analog.GR_GAUSSIAN, math.sqrt( 0.5 / ( math.pow(10, eb_no_db/10) ) ), 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, math.sqrt( 0.5 / ( math.pow(10, eb_no_db/10) ) ), 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_noise_source_x_0_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.wes_ber_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.wes_ber_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.digital_constellation_decoder_cb_0_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.wes_ber_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.wes_ber_0_0, 1))
        self.connect((self.wes_ber_0, 1), (self.qtgui_number_sink_0_0_0_0, 1))
        self.connect((self.wes_ber_0, 0), (self.qtgui_number_sink_0_0_0_0, 0))
        self.connect((self.wes_ber_0_0, 1), (self.qtgui_number_sink_0_0_0_0_0, 1))
        self.connect((self.wes_ber_0_0, 0), (self.qtgui_number_sink_0_0_0_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lab5_qpsk")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_reset_ber(self):
        return self.reset_ber

    def set_reset_ber(self, reset_ber):
        self.reset_ber = reset_ber
        self.wes_ber_0.reset_stats(self.reset_ber)
        self.wes_ber_0_0.reset_stats(self.reset_ber)

    def get_frame_size(self):
        return self.frame_size

    def set_frame_size(self, frame_size):
        self.frame_size = frame_size

    def get_eb_no_db(self):
        return self.eb_no_db

    def set_eb_no_db(self, eb_no_db):
        self.eb_no_db = eb_no_db
        self.analog_noise_source_x_0.set_amplitude(math.sqrt( 0.5 / ( math.pow(10, self.eb_no_db/10) ) ))
        self.analog_noise_source_x_0_0.set_amplitude(math.sqrt( 0.5 / ( math.pow(10, self.eb_no_db/10) ) ))

    def get_const_non_gray(self):
        return self.const_non_gray

    def set_const_non_gray(self, const_non_gray):
        self.const_non_gray = const_non_gray

    def get_const_gray(self):
        return self.const_gray

    def set_const_gray(self, const_gray):
        self.const_gray = const_gray



def main(top_block_cls=lab5_qpsk, options=None):

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
