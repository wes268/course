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
#include "alamouti_cc_impl.h"

namespace gr {
  namespace ofdm {

    alamouti_cc::sptr
    alamouti_cc::make(float p_xy, float std_dev, int mimo_option)
    {
      return gnuradio::get_initial_sptr
        (new alamouti_cc_impl(p_xy, std_dev, mimo_option));
    }

    static int ios[] = { sizeof(gr_complex), sizeof(gr_complex), sizeof(float) };
    static std::vector<int> iosig(ios, ios + sizeof(ios) / sizeof(int));
    /*
     * The private constructor
     */
    alamouti_cc_impl::alamouti_cc_impl(float p_xy, float std_dev, int mimo_option)
      : gr::block("alamouti_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::makev(1, 3, iosig )),
              d_p_xy(p_xy),
              d_rng(0),
              d_std_dev(std_dev),
              d_mimo_option(mimo_option)
    {
        d_p_xy = 0;
        d_mimo_option = mimo_option;
    }

    /*
     * Our virtual destructor.
     */
    alamouti_cc_impl::~alamouti_cc_impl()
    {
    }

    void
    alamouti_cc_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
      ninput_items_required[0] = floor(noutput_items/2);
    }

    int
    alamouti_cc_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      // inputs
      const gr_complex *in = (const gr_complex *) input_items[0];

      //////////////
      // outputs ///
      //////////////

      // correlated output
      gr_complex *out1 = (gr_complex *) output_items[0];

      // de-correlated outputs
      gr_complex *out2 = output_items.size() >= 2 ? (gr_complex *) output_items[1] : NULL;

      // eigenvalues out
      float *out_eigen = output_items.size() >= 3 ? (float *) output_items[2] : NULL;

      // inits
      int nSymbols = floor(noutput_items/2);
      gr_complex h1, h2, n1, n2, temp, e1c, e2c, h11, h12, h21, h22, inv_den;
      gr_complex HH11, HH12, HH21, HH22;
      float h1_mag2, h2_mag2, C1, C2, tempf, b2_4ac;
      float K = 0.707;
      C1 = sqrt(1.0-d_p_xy);
      C2 = sqrt(1.0+d_p_xy);

      for( int n=0; n < nSymbols; n++)
      {
          if( d_mimo_option == 0 ){
              // initialize ch. parameters
              h1 = gr_complex( C1*K*d_rng.gasdev(), C1*K*d_rng.gasdev());
              h2 = gr_complex( C2*K*d_rng.gasdev(), C2*K*d_rng.gasdev());
              n1 = gr_complex( d_std_dev*d_rng.gasdev(), d_std_dev*d_rng.gasdev());
              n2 = gr_complex( d_std_dev*d_rng.gasdev(), d_std_dev*d_rng.gasdev());

              // create and correlated channel
              temp = h1;
              h1 = gr_complex(K,0)*(h2-h1);
              h2 = gr_complex(K,0)*(h2+temp);

              // create h1 and h2 magnitude squareds
              h1_mag2 = h1.real()*h1.real() + h1.imag()*h1.imag();
              h2_mag2 = h2.real()*h2.real() + h2.imag()*h2.imag();

              // correlate symbols
              out1[2*n]     =   h1*in[2*n] - h2*in[2*n+1] + n1;
              out1[2*n+1]   =   h1*conj(in[2*n+1]) + h2*conj(in[2*n]) + n2;

              // de-correlate symbols
              out2[2*n+1]   =   conj(out1[2*n+1]);  // set y[1] equal to y*[1]

              out2[2*n]     =  (  conj(h1)*out1[2*n] + h2*out2[2*n+1]  ) / ( h1_mag2 + h2_mag2 );
              out2[2*n+1]   =  ( -conj(h2)*out1[2*n] + h1*out2[2*n+1]  ) / ( h1_mag2 + h2_mag2 );

              // output eigenvalues
              b2_4ac = h1.real()*h1.real()-(h1_mag2+h2_mag2);

              // b^2-4ac check for negative values
              if( b2_4ac >= 0 ) {
                  out_eigen[2*n]    =   abs(h1.real() + sqrt( b2_4ac ));
                  out_eigen[2*n+1]  =   abs(h1.real() - sqrt( b2_4ac ));
              }
              else
              {
                  e1c               =   gr_complex(h1.real(),sqrt( -b2_4ac ));
                  e2c               =   gr_complex(h1.real(),-sqrt( -b2_4ac ));
                  out_eigen[2*n]    =   sqrt( e1c.real()*e1c.real() + e1c.imag()*e1c.imag() );
                  out_eigen[2*n+1]  =   sqrt( e2c.real()*e2c.real() + e2c.imag()*e2c.imag() );
              }

              // ensure first eigenvalue is the largest one
              if( out_eigen[2*n] < out_eigen[2*n+1] ){
                  tempf = out_eigen[2*n];
                  out_eigen[2*n] = out_eigen[2*n+1];
                  out_eigen[2*n+1] = tempf;
              }
          } // if( mimo_option == 0)
          else
          {
              // initialize ch. parameters
              // generate a random scattering pattern
              h11 = gr_complex(sqrt(abs(1-d_p_xy)),0)*gr_complex( K*d_rng.gasdev(), K*d_rng.gasdev());
              h12 = gr_complex(sqrt(abs(1-d_p_xy)),0)*gr_complex( K*d_rng.gasdev(), K*d_rng.gasdev());
              h21 = gr_complex(sqrt(abs(1-d_p_xy)),0)*gr_complex( K*d_rng.gasdev(), K*d_rng.gasdev());
              h22 = gr_complex(sqrt(abs(1-d_p_xy)),0)*gr_complex( K*d_rng.gasdev(), K*d_rng.gasdev());

              // generate a LOS path
              h11 = h11 + gr_complex(d_p_xy,0);
              h12 = h12 + gr_complex(d_p_xy,0);
              h21 = h21 + gr_complex(d_p_xy,0);
              h22 = h22 + gr_complex(d_p_xy,0);

              n1 = gr_complex( d_std_dev*d_rng.gasdev(), d_std_dev*d_rng.gasdev());
              n2 = gr_complex( d_std_dev*d_rng.gasdev(), d_std_dev*d_rng.gasdev());

              // correlate symbols
              out1[2*n]     =   h11*in[2*n]   +   h12*in[2*n+1]     + n1;
              out1[2*n+1]   =   h21*in[2*n]   +   h22*in[2*n+1]     + n2;

              // de-correlate symbols
              out2[2*n]     =  h22*out1[2*n] - h12*out1[2*n+1];
              out2[2*n+1]   = -h21*out1[2*n] + h11*out1[2*n+1];
              inv_den       =  h11*h22 - h12*h21;

              out2[2*n]     = out2[2*n] / inv_den;
              out2[2*n+1]   = out2[2*n+1] / inv_den;

              HH11 = h11*conj(h11) + h21*conj(h21);
              HH12 = conj(h11)*h12 + conj(h21)*h22;
              HH21 = h11*conj(h12) + h21*conj(h22);
              HH22 = h12*conj(h12) + h22*conj(h22);


              e1c = (HH11+HH12) + sqrt( (HH11+HH12)*(HH11+HH12) - gr_complex(4,0)*(HH11*HH22-HH12*conj(HH12)) );
              e2c = (HH11+HH12) - sqrt( (HH11+HH12)*(HH11+HH12) - gr_complex(4,0)*(HH11*HH22-HH12*conj(HH12)) );

              out_eigen[2*n]    = sqrt( e1c.real()*e1c.real() + e1c.imag()*e1c.imag() );
              out_eigen[2*n+1]  = sqrt( e2c.real()*e1c.real() + e2c.imag()*e2c.imag() );

              // ensure first eigenvalue is the largest one
              if( out_eigen[2*n] < out_eigen[2*n+1] ){
                  tempf = out_eigen[2*n];
                  out_eigen[2*n] = out_eigen[2*n+1];
                  out_eigen[2*n+1] = tempf;
              }
          }

      } // for( ... )

      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (nSymbols);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

    void alamouti_cc_impl::set_p_xy( float p_xy ){
        d_p_xy = p_xy;
    }

    void alamouti_cc_impl::set_noise( float std_dev ){
        d_std_dev = std_dev;
    }

    void alamouti_cc_impl::set_mimo_option( int mimo_option ){
        d_mimo_option = mimo_option;
    }
  } /* namespace ofdm */
} /* namespace gr */
