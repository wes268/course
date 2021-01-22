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
#include "hamming_decoder_impl.h"

namespace gr {
  namespace wes {

    hamming_decoder::sptr
    hamming_decoder::make(int frame_size)
    {
      return gnuradio::get_initial_sptr
        (new hamming_decoder_impl(frame_size));
    }

    /*
     * The private constructor
     */
    hamming_decoder_impl::hamming_decoder_impl(int frame_size)
      : gr::block("hamming_decoder",
              gr::io_signature::make(1, 1, sizeof(char)),
              gr::io_signature::make(1, 1, sizeof(char))),
              d_frame_size(frame_size)
    {}

    /*
     * Our virtual destructor.
     */
    hamming_decoder_impl::~hamming_decoder_impl()
    {
    }

    void
    hamming_decoder_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
      ninput_items_required[0] = d_frame_size;
    }

    int
    hamming_decoder_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const char *in = (const char *) input_items[0];
      char *out = (char *) output_items[0];

      // code parameters
      int n = 7;
      int k = 4;

      // s is the syndrome vector
      int s[3] = {0,0,0};
      int result = 0;
      int temp = 0;
      int idx = 0;

      // parity check matrix
      int H[3][7] = {
          {1, 0, 1, 1, 1, 0, 0} ,
          {1, 1, 0, 1, 0, 1, 0} ,
          {0, 1, 1, 1, 0, 0, 1}
      };

      // note: d_frame_size should be a multiple of n
      int nBlocks = floor(d_frame_size / n);

      // Hamming Decoder
      //
      //        [1 0 1 1 1 0 0]
      //  H =   [1 1 0 1 0 1 0]
      //        [0 1 1 1 0 0 1]
      //

      // processing / decoding loop
      for( int i=0; i < nBlocks; i++){

          // calculate syndrome
          s[0] = in[i*n+0] ^ in[i*n+2] ^ in[i*n+3] ^ in[i*n+4];
          s[1] = in[i*n+0] ^ in[i*n+1] ^ in[i*n+3] ^ in[i*n+5];
          s[2] = in[i*n+1] ^ in[i*n+2] ^ in[i*n+3] ^ in[i*n+6];

          // syndrome result
          result = s[0] | s[1] | s[2];

          // find correct code word
          if( result == 0 )
          {
              out[i*k+0] = in[i*n+0];
              out[i*k+1] = in[i*n+1];
              out[i*k+2] = in[i*n+2];
              out[i*k+3] = in[i*n+3];
          }
          else
          {
              // search H matrix for syndrome match
              temp = 0;
              idx = 0;
              for(int j=0; j < n; j++){

                  temp =  (s[0] ^ H[0][j]) | (s[1] ^ H[1][j]) | (s[2] ^ H[2][j]);
                  if( temp == 0 )
                  {
                      idx = j;
                      break;
                  }
              }

              out[i*k+0] = in[i*n+0];
              out[i*k+1] = in[i*n+1];
              out[i*k+2] = in[i*n+2];
              out[i*k+3] = in[i*n+3];

              if( idx < 4){
                  if( out[i*k+idx] == 0 ){
                      out[i*k+idx] = 1;
                  }
                  else{
                      out[i*k+idx] = 0;
                  }
              }
          }
      } // for

      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (d_frame_size);

      // Tell runtime system how many output items we produced.
      return floor( nBlocks * k );
    }

  } /* namespace wes */
} /* namespace gr */
