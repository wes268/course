/* -*- c++ -*- */
/*
 * Copyright 2021 pling.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "max_ff_impl.h"

namespace gr {
  namespace wes {

    max_ff::sptr
    max_ff::make(int frame_len)
    {
      return gnuradio::get_initial_sptr
        (new max_ff_impl(frame_len));
    }


    /*
     * The private constructor
     */
    max_ff_impl::max_ff_impl(int frame_len)
      : gr::block("max_ff",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(float))),
              d_frame_len(frame_len)
    {
        d_frame_len = frame_len;
        d_max_val = 0;
    }

    /*
     * Our virtual destructor.
     */
    max_ff_impl::~max_ff_impl()
    {
    }

    void
    max_ff_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
      ninput_items_required[0] = d_frame_len;
    }

    int
    max_ff_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];

      float max_val = 0;

      // Do <+signal processing+>
      for( int n=0; n < d_frame_len; n++){
          if( in[n] > max_val ){
            max_val = in[n];
          }

          //out[n] = d_max_val;
      }

      for( int n=0; n < d_frame_len; n++){
          out[n] = max_val;
      }

      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (d_frame_len);

      // Tell runtime system how many output items we produced.
      return d_frame_len;
    }

  } /* namespace wes */
} /* namespace gr */
