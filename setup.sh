#!/usr/bin/env bash

# copy .hier file cache
echo "Installing Hier Files..."

# copy hier files
cp -r hier_cache/* ~/.grc_gnuradio

# OOT module wes
cd oot/gr-wes

rm -rf build
mkdir build
cd build
cmake ..
make
sudo make install

sudo ldconfig

cd ../../gr-ofdm

rm -rf build
mkdir build
cd build
cmake ..
make
sudo make install

sudo ldconfig

echo "Code Compilation Complete... "
echo "Blocks Updated..."
