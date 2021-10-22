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

#ifndef INCLUDED_OFDM_ALAMOUTI_CC_IMPL_H
#define INCLUDED_OFDM_ALAMOUTI_CC_IMPL_H

#include <ofdm/alamouti_cc.h>
#include <gnuradio/random.h>

namespace gr {
  namespace ofdm {

    class alamouti_cc_impl : public alamouti_cc
    {
     private:
      // Nothing to declare in this block.
     float d_p_xy;
     gr::random d_rng;
     float d_std_dev;
     int d_mimo_option;

     public:
      alamouti_cc_impl(float p_xy, float std_dev, int mimo_option);
      ~alamouti_cc_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

      void set_p_xy(float p_xy);
      void set_noise(float std_dev);
      void set_mimo_option(int mimo_option);

    };

  } // namespace ofdm
} // namespace gr

#endif /* INCLUDED_OFDM_ALAMOUTI_CC_IMPL_H */
