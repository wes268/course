/* -*- c++ -*- */

#define WES_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "wes_swig_doc.i"

%{
#include "wes/costas_cc.h"
#include "wes/ber.h"
#include "wes/hamming_encoder.h"
#include "wes/hamming_decoder.h"
#include "wes/max_ff.h"
%}

%include "wes/costas_cc.h"
GR_SWIG_BLOCK_MAGIC2(wes, costas_cc);
%include "wes/ber.h"
GR_SWIG_BLOCK_MAGIC2(wes, ber);
%include "wes/hamming_encoder.h"
GR_SWIG_BLOCK_MAGIC2(wes, hamming_encoder);

%include "wes/hamming_decoder.h"
GR_SWIG_BLOCK_MAGIC2(wes, hamming_decoder);
%include "wes/max_ff.h"
GR_SWIG_BLOCK_MAGIC2(wes, max_ff);
