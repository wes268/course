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

#ifndef INCLUDED_WES_MAX_FF_H
#define INCLUDED_WES_MAX_FF_H

#include <wes/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace wes {

    /*!
     * \brief <+description of block+>
     * \ingroup wes
     *
     */
    class WES_API max_ff : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<max_ff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of wes::max_ff.
       *
       * To avoid accidental use of raw pointers, wes::max_ff's
       * constructor is in a private implementation
       * class. wes::max_ff::make is the public interface for
       * creating new instances.
       */
      static sptr make(int frame_len);
    };

  } // namespace wes
} // namespace gr

#endif /* INCLUDED_WES_MAX_FF_H */

