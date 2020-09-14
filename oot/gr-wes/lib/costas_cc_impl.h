/* -*- c++ -*- */
/*
 * Copyright 2020 pling.
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

#ifndef INCLUDED_WES_COSTAS_CC_IMPL_H
#define INCLUDED_WES_COSTAS_CC_IMPL_H

#include <wes/costas_cc.h>
#include <gnuradio/io_signature.h>
#include <gnuradio/expj.h>
#include <gnuradio/math.h>
#include <gnuradio/sincos.h>

namespace gr {
  namespace wes {

    class costas_cc_impl : public costas_cc
    {
     private:
         float d_natural_freq;
         float d_zeta;
         int d_loop_type;

     public:
      costas_cc_impl(float fn, float zeta, int loop_type);
      ~costas_cc_impl();

      // Where all the action really happens
      int work(
              int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace wes
} // namespace gr

#endif /* INCLUDED_WES_COSTAS_CC_IMPL_H */