#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Hamming and n-Repetition
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
from gnuradio import fec
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

class lab5(gr.top_block, Qt.QWidget):

    def __init__(self, frame_size=4096, puncpat='11'):
        gr.top_block.__init__(self, "Hamming and n-Repetition")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Hamming and n-Repetition")
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

        self.settings = Qt.QSettings("GNU Radio", "lab5")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.frame_size = frame_size
        self.puncpat = puncpat

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32e3
        self.reset_ber = reset_ber = 0
        self.enc_rep = enc_rep = fec.repetition_encoder_make(frame_size, 3)
        self.eb_no_db = eb_no_db = 10
        self.dec_rep = dec_rep = fec.repetition_decoder.make(frame_size,3, 0.5)
        self.R_rep = R_rep = 1/3
        self.R_hamming = R_hamming = 4/7

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
        self.wes_hamming_encoder_0 = wes.hamming_encoder(frame_size)
        self.wes_hamming_decoder_0 = wes.hamming_decoder(int(frame_size *7/4))
        self.wes_ber_0_0_0_0 = wes.ber(1, reset_ber)
        self.wes_ber_0_0_0 = wes.ber(1, reset_ber)
        self.wes_ber_0 = wes.ber(1, reset_ber)
        self.qtgui_number_sink_0_0_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            2
        )
        self.qtgui_number_sink_0_0_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0_0_0.set_title("Uncoded")

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
        self.qtgui_number_sink_0_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            2
        )
        self.qtgui_number_sink_0_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0_0.set_title("Hamming (7,4)")

        labels = ['BER', '# Errors', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(2):
            self.qtgui_number_sink_0_0_0.set_min(i, -1)
            self.qtgui_number_sink_0_0_0.set_max(i, 1)
            self.qtgui_number_sink_0_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_0_0_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            2
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("n-Repetition")

        labels = ['BER', '# Errors', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(2):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win)
        self.fec_extended_encoder_1_0_0 = fec.extended_encoder(encoder_obj_list=enc_rep, threading= None, puncpat=puncpat)
        self.fec_extended_decoder_0_1_0 = fec.extended_decoder(decoder_obj_list=dec_rep, threading= None, ann=None, puncpat=puncpat, integration_period=10000)
        self.digital_map_bb_0_0_1_1_0 = digital.map_bb([-1, 1])
        self.digital_map_bb_0_0_1_1 = digital.map_bb([-1, 1])
        self.digital_map_bb_0_0_0_0 = digital.map_bb([-1, 1])
        self.digital_map_bb_0 = digital.map_bb([-1, 1])
        self.digital_binary_slicer_fb_0_0_0_0 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0_0_0 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_char_to_float_0_2_0_0_0_0_1_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_2_0_0_0_0_1 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_2_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_2_0 = blocks.char_to_float(1, 1)
        self.blocks_add_xx_0_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2, frame_size))), True)
        self.analog_random_source_x_0.set_min_output_buffer(4096)
        self.analog_random_source_x_0.set_max_output_buffer(4096)
        self.analog_noise_source_x_0_0_0_0 = analog.noise_source_f(analog.GR_GAUSSIAN, math.sqrt( 0.5 / ( 1* math.pow(10, eb_no_db/10) ) ), 0)
        self.analog_noise_source_x_0_0_0 = analog.noise_source_f(analog.GR_GAUSSIAN, math.sqrt( 0.5 / ( R_hamming * math.pow(10, eb_no_db/10) ) ), 0)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, math.sqrt( 0.5 / ( R_rep * math.pow(10, eb_no_db/10) ) ), 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_noise_source_x_0_0_0, 0), (self.blocks_add_xx_0_0_0, 1))
        self.connect((self.analog_noise_source_x_0_0_0_0, 0), (self.blocks_add_xx_0_0_0_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_map_bb_0_0_1_1_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.fec_extended_encoder_1_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.wes_ber_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.wes_ber_0_0_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.wes_ber_0_0_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.wes_hamming_encoder_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_add_xx_0_0_0, 0), (self.digital_binary_slicer_fb_0_0_0, 0))
        self.connect((self.blocks_add_xx_0_0_0_0, 0), (self.digital_binary_slicer_fb_0_0_0_0, 0))
        self.connect((self.blocks_char_to_float_0_2_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_char_to_float_0_2_0_0, 0), (self.fec_extended_decoder_0_1_0, 0))
        self.connect((self.blocks_char_to_float_0_2_0_0_0_0_1, 0), (self.blocks_add_xx_0_0_0, 0))
        self.connect((self.blocks_char_to_float_0_2_0_0_0_0_1_0, 0), (self.blocks_add_xx_0_0_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_0_0, 0), (self.wes_hamming_decoder_0, 0))
        self.connect((self.digital_binary_slicer_fb_0_0_0_0, 0), (self.wes_ber_0_0_0_0, 1))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_char_to_float_0_2_0_0, 0))
        self.connect((self.digital_map_bb_0_0_0_0, 0), (self.blocks_char_to_float_0_2_0, 0))
        self.connect((self.digital_map_bb_0_0_1_1, 0), (self.blocks_char_to_float_0_2_0_0_0_0_1, 0))
        self.connect((self.digital_map_bb_0_0_1_1_0, 0), (self.blocks_char_to_float_0_2_0_0_0_0_1_0, 0))
        self.connect((self.fec_extended_decoder_0_1_0, 0), (self.wes_ber_0, 0))
        self.connect((self.fec_extended_encoder_1_0_0, 0), (self.digital_map_bb_0_0_0_0, 0))
        self.connect((self.wes_ber_0, 1), (self.qtgui_number_sink_0, 1))
        self.connect((self.wes_ber_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.wes_ber_0_0_0, 0), (self.qtgui_number_sink_0_0_0, 0))
        self.connect((self.wes_ber_0_0_0, 1), (self.qtgui_number_sink_0_0_0, 1))
        self.connect((self.wes_ber_0_0_0_0, 1), (self.qtgui_number_sink_0_0_0_0, 1))
        self.connect((self.wes_ber_0_0_0_0, 0), (self.qtgui_number_sink_0_0_0_0, 0))
        self.connect((self.wes_hamming_decoder_0, 0), (self.wes_ber_0_0_0, 0))
        self.connect((self.wes_hamming_encoder_0, 0), (self.digital_map_bb_0_0_1_1, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lab5")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_frame_size(self):
        return self.frame_size

    def set_frame_size(self, frame_size):
        self.frame_size = frame_size

    def get_puncpat(self):
        return self.puncpat

    def set_puncpat(self, puncpat):
        self.puncpat = puncpat

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_reset_ber(self):
        return self.reset_ber

    def set_reset_ber(self, reset_ber):
        self.reset_ber = reset_ber
        self.wes_ber_0.reset_stats(self.reset_ber)
        self.wes_ber_0_0_0.reset_stats(self.reset_ber)
        self.wes_ber_0_0_0_0.reset_stats(self.reset_ber)

    def get_enc_rep(self):
        return self.enc_rep

    def set_enc_rep(self, enc_rep):
        self.enc_rep = enc_rep

    def get_eb_no_db(self):
        return self.eb_no_db

    def set_eb_no_db(self, eb_no_db):
        self.eb_no_db = eb_no_db
        self.analog_noise_source_x_0.set_amplitude(math.sqrt( 0.5 / ( self.R_rep * math.pow(10, self.eb_no_db/10) ) ))
        self.analog_noise_source_x_0_0_0.set_amplitude(math.sqrt( 0.5 / ( self.R_hamming * math.pow(10, self.eb_no_db/10) ) ))
        self.analog_noise_source_x_0_0_0_0.set_amplitude(math.sqrt( 0.5 / ( 1* math.pow(10, self.eb_no_db/10) ) ))

    def get_dec_rep(self):
        return self.dec_rep

    def set_dec_rep(self, dec_rep):
        self.dec_rep = dec_rep

    def get_R_rep(self):
        return self.R_rep

    def set_R_rep(self, R_rep):
        self.R_rep = R_rep
        self.analog_noise_source_x_0.set_amplitude(math.sqrt( 0.5 / ( self.R_rep * math.pow(10, self.eb_no_db/10) ) ))

    def get_R_hamming(self):
        return self.R_hamming

    def set_R_hamming(self, R_hamming):
        self.R_hamming = R_hamming
        self.analog_noise_source_x_0_0_0.set_amplitude(math.sqrt( 0.5 / ( self.R_hamming * math.pow(10, self.eb_no_db/10) ) ))


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--frame-size", dest="frame_size", type=intx, default=4096,
        help="Set Frame Size [default=%(default)r]")
    return parser


def main(top_block_cls=lab5, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(frame_size=options.frame_size)
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
