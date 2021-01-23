# README

## Quick Setup Instructions

Cloning Instructions:

    git clone https://github.com/wes268/course

To begin with, make sure to run the install script

    ./setup.sh

Note: this will require you to enter the password for sudo mode

## Adding Python Paths for Manual Installations

add the following three lines to your .profile or .bashrc file in your home directory

    # gnuradio
    export PYTHONPATH=$PYTHONPATH:/usr/lib/python3/dist-packages/gnuradio
    export PYTHONPATH=$PYTHONPATH:/usr/lib/python3/dist-packages/
    export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3/dist-packages/

## Updating the firmware to AD9364

In order to detect FM band signals we need to change the firmware so that the plutoSDR is recognized as a AD9364, this allows for a frequency range to 70Mhz to 6GHz

Details on how to change this can be found here:

    wiki.analog.com/university/tools/pluto/users/customizing

This will require you to make an ssh or serial connection to the pluto device. The username/password are shown below:

    -user: root
    -password: analog

For this tutorial, we'll show you how to ssh into the device:

    ssh root@192.168.2.2

After you have logged in by ssh, type the following commands:

    # fw_setenv attr_name compatible
    # fw_setenv attr_val ad9364
    # reboot

After rebooting you should see the following outputs

    # fw_printenv attr_name
    attr_name=compatible
    # fw_printenv attr_val
    attr_val=ad9364

This is how you know whether the firmware update was successful or not.


