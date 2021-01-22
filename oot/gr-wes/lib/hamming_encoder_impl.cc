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
#include "hamming_encoder_impl.h"

namespace gr {
  namespace wes {

    hamming_encoder::sptr
    hamming_encoder::make(int frame_size)
    {
      return gnuradio::get_initial_sptr
        (new hamming_encoder_impl(frame_size));
    }


    /*
     * The private constructor
     */
    hamming_encoder_impl::hamming_encoder_impl(int frame_size)
      : gr::block("hamming_encoder",
              gr::io_signature::make(1, 1, sizeof(char)),
              gr::io_signature::make(1, 1, sizeof(char))),
              d_frame_size(frame_size)
    {

    }

    /*
     * Our virtual destructor.
     */
    hamming_encoder_impl::~hamming_encoder_impl()
    {
    }

    void
    hamming_encoder_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
      ninput_items_required[0] = d_frame_size;

      // Note: d_frame_size should be a multiple of 4
    }

    int
    hamming_encoder_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const char *in = (const char *) input_items[0];
      char *out = (char *) output_items[0];

      // code params hamming (n,k) = (7,4)
      int n = 7;        // code block size n
      int k = 4;        // info block size k

      // d_frame_size should be a multiple of 4
      int nBlocks = floor(d_frame_size / k);

      // Hamming Encoder
      //
      //        [1 0 1 1 1 0 0]
      //  H =   [1 1 0 1 0 1 0]
      //        [0 1 1 1 0 0 1]
      //

      for( int i=0; i < nBlocks; i++){

          // info bits
          out[i*n+0] = in[i*k+0];
          out[i*n+1] = in[i*k+1];
          out[i*n+2] = in[i*k+2];
          out[i*n+3] = in[i*k+3];

          // parity bits
          out[i*n+4] = in[i*k+0] ^ in[i*k+2] ^ in[i*k+3];
          out[i*n+5] = in[i*k+0] ^ in[i*k+1] ^ in[i*k+3];
          out[i*n+6] = in[i*k+1] ^ in[i*k+2] ^ in[i*k+3];
      }

      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (d_frame_size);

      // Tell runtime system how many output items we produced.
      return floor(nBlocks * n);
    }

  } /* namespace wes */
} /* namespace gr */
