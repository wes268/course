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
#include "pilot_comp_cc_impl.h"

namespace gr {
  namespace ofdm {

    pilot_comp_cc::sptr
    pilot_comp_cc::make(int fft_len, int apply_comp, int num_syms)
    {
      return gnuradio::get_initial_sptr
        (new pilot_comp_cc_impl(fft_len, apply_comp, num_syms));
    }


    /*
     * The private constructor
     */
    pilot_comp_cc_impl::pilot_comp_cc_impl(int fft_len, int apply_comp, int num_syms)
      : gr::block("pilot_comp_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex))),
              d_fft_len(fft_len),
              d_apply_comp(apply_comp),
              d_num_syms(num_syms)
    {
        if( num_syms <= 0)
            d_num_syms = 32;

        // set tag policy
        set_relative_rate(1, 1);
        // Really, we have TPP_ONE_TO_ONE, but the channel state is not propagated
        set_tag_propagation_policy(TPP_ALL_TO_ALL);
    }

    /*
     * Our virtual destructor.
     */
    pilot_comp_cc_impl::~pilot_comp_cc_impl()
    {
    }

    void
    pilot_comp_cc_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
      ninput_items_required[0] = d_fft_len * d_num_syms;
    }

    int
    pilot_comp_cc_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const gr_complex *in = (const gr_complex *) input_items[0];
        gr_complex *out = (gr_complex *) output_items[0];

        // inits
        gr_complex p1,p2,p3,p4,phase_est,phase_correct;

        float pI,pQ,pMag;
        int   n1 = 11,
              n2 = 11 + 14,
              n3 = 11 + 14 + 14,
              n4 = 11 + 14 + 14 + 14;

        // Do <+signal processing+>
        for( int n=0; n < d_num_syms; n++){
            p1 = in[ n*d_fft_len + n1];
            p2 = in[ n*d_fft_len + n2];
            p3 = in[ n*d_fft_len + n3];
            p4 = in[ n*d_fft_len + n4] * gr_complex(-1,0);

            phase_est = (p1+p2+p3+p4) / gr_complex(4,0);

            pI = phase_est.real();
            pQ = phase_est.imag();
            pMag = sqrt(pI*pI + pQ*pQ);

            pI = pI / pMag;
            pQ = pQ / pMag;

            phase_correct = gr_complex(pI,pQ);

            for( int m=0; m < d_fft_len; m++){
                if( d_apply_comp == 1 ){
                  out[ n*d_fft_len + m ] = in[ n*d_fft_len + m ] * conj(phase_correct);
                }
                else{
                  out[ n*d_fft_len + m ] = in[ n*d_fft_len + m ];
                }
            } // for( int m=0; m < d_fft_len; m++){
        } // for( int n=0; n < d_num_syms; n++){

        // Tell runtime system how many input items we consumed on
        // each input stream.
        consume_each (d_fft_len * d_num_syms);

        // Tell runtime system how many output items we produced.
        return (d_fft_len * d_num_syms);

      // Do <+signal processing+>
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (noutput_items);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

    void
    pilot_comp_cc_impl::toggle_comp(int apply_comp){
        d_apply_comp = apply_comp;
    }
  } /* namespace ofdm */
} /* namespace gr */
