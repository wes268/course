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

#ifndef INCLUDED_OFDM_PILOT_COMP_CC_IMPL_H
#define INCLUDED_OFDM_PILOT_COMP_CC_IMPL_H

#include <ofdm/pilot_comp_cc.h>

namespace gr {
  namespace ofdm {

    class pilot_comp_cc_impl : public pilot_comp_cc
    {
     private:
      // Nothing to declare in this block.
      int d_fft_len;
      int d_apply_comp;
      int d_num_syms;

     public:
      pilot_comp_cc_impl(int fft_len, int apply_comp, int num_syms);
      ~pilot_comp_cc_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

      void toggle_comp(int apply_comp);
    };

  } // namespace ofdm
} // namespace gr

#endif /* INCLUDED_OFDM_PILOT_COMP_CC_IMPL_H */
