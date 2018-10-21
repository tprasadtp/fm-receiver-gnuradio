#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Wideband FM Receiver 1.0
# Author: Prasad Tengse
# Description: Wideband FM Receiver for RTL SRD Radio. Options to Tune several parameters.
# Generated: Sun Oct 21 03:46:42 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class RTL_SDR_FM_Radio(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Wideband FM Receiver 1.0")
        _icon_path = "C:\Program Files\GNURadio-3.7\share\icons\hicolor\scalable/apps\gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.gain = gain = 50
        self.fft_size = fft_size = 512
        self.f = f = 106.1e6

        ##################################################
        # Blocks
        ##################################################
        self.notebook0 = self.notebook0 = wx.Notebook(self.GetWin(), style=wx.NB_BOTTOM)
        self.notebook0.AddPage(grc_wxgui.Panel(self.notebook0), "RF FFT")
        self.notebook0.AddPage(grc_wxgui.Panel(self.notebook0), "Waterfall")
        self.notebook0.AddPage(grc_wxgui.Panel(self.notebook0), "Audio FFT")
        self.Add(self.notebook0)
        self._fft_size_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.fft_size,
        	callback=self.set_fft_size,
        	label='FFT Size',
        	choices=[512, 1024, 2048, 4096,8192],
        	labels=[],
        	style=wx.RA_HORIZONTAL,
        )
        self.Add(self._fft_size_chooser)
        _f_sizer = wx.BoxSizer(wx.VERTICAL)
        self._f_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_f_sizer,
        	value=self.f,
        	callback=self.set_f,
        	label='f',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._f_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_f_sizer,
        	value=self.f,
        	callback=self.set_f,
        	minimum=88e6,
        	maximum=110e6,
        	num_steps=220,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.Add(_f_sizer)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.notebook0.GetPage(1).GetWin(),
        	baseband_freq=f,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=fft_size,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='Waterfall Plot',
        )
        self.notebook0.GetPage(1).Add(self.wxgui_waterfallsink2_0.win)
        self.wxgui_fftsink2_1 = fftsink2.fft_sink_f(
        	self.notebook0.GetPage(2).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=200e3,
        	fft_size=2048,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot - Audio',
        	peak_hold=False,
        	win=window.rectangular,
        )
        self.notebook0.GetPage(2).Add(self.wxgui_fftsink2_1.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.notebook0.GetPage(0).GetWin(),
        	baseband_freq=f,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=fft_size,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        	win=window.blackmanharris,
        )
        self.notebook0.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_clock_source('internal', 0)
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(f, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(1, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(5, 0)
        self.rtlsdr_source_0.set_if_gain(5, 0)
        self.rtlsdr_source_0.set_bb_gain(5, 0)
        self.rtlsdr_source_0.set_antenna('ant0', 0)
        self.rtlsdr_source_0.set_bandwidth(250000, 0)

        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=100,
                decimation=441,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(20, firdes.low_pass(
        	1, samp_rate, 100e3, 10e3, firdes.WIN_BLACKMAN, 6.76))
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label='Gain Control',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=0,
        	maximum=100,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_gain_sizer)
        self.audio_sink_0 = audio.sink(44100, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=100e3,
        	audio_decimation=1,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.wxgui_fftsink2_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.wxgui_waterfallsink2_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 10e3, firdes.WIN_BLACKMAN, 6.76))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size
        self._fft_size_chooser.set_value(self.fft_size)

    def get_f(self):
        return self.f

    def set_f(self, f):
        self.f = f
        self._f_slider.set_value(self.f)
        self._f_text_box.set_value(self.f)
        self.wxgui_waterfallsink2_0.set_baseband_freq(self.f)
        self.wxgui_fftsink2_0.set_baseband_freq(self.f)
        self.rtlsdr_source_0.set_center_freq(self.f, 0)


def main(top_block_cls=RTL_SDR_FM_Radio, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
