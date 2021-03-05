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

#ifndef INCLUDED_OFDM_ALAMOUTI_CC_H
#define INCLUDED_OFDM_ALAMOUTI_CC_H

#include <ofdm/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace ofdm {

    /*!
     * \brief <+description of block+>
     * \ingroup ofdm
     *
     */
    class OFDM_API alamouti_cc : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<alamouti_cc> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of ofdm::alamouti_cc.
       *
       * To avoid accidental use of raw pointers, ofdm::alamouti_cc's
       * constructor is in a private implementation
       * class. ofdm::alamouti_cc::make is the public interface for
       * creating new instances.
       */
      static sptr make(float p_xy, float std_dev, int mimo_option);

      virtual void set_p_xy(float p_xy) = 0;
      virtual void set_noise(float std_dev) = 0;
      virtual void set_mimo_option(int mimo_option) = 0;
    };

  } // namespace ofdm
} // namespace gr

#endif /* INCLUDED_OFDM_ALAMOUTI_CC_H */
