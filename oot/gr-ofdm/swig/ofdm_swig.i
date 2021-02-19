/* -*- c++ -*- */

#define OFDM_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "ofdm_swig_doc.i"

%{
#include "ofdm/pilot_comp_cc.h"
%}

%include "ofdm/pilot_comp_cc.h"
GR_SWIG_BLOCK_MAGIC2(ofdm, pilot_comp_cc);
