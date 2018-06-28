#-*- coding: utf-8 -*-

#**********************************************************************
# Script name: obseis_convert.py
# Version: 2018.06.28
# Description: Python script for converting seismograms between file
#   formats supported by ObsPy.
#
# Author: Gregor Rajh
# Year: 2018
# Python version: 2 and 3
# Requirements:
#   *obspy and its dependencies
#
# e-mail: rajhgregor@gmail.com
#**********************************************************************

import obspy
import os
from obspy import read
from os import path
import time

start_time = time.clock()

input_file_folder = "/home/gregor/Documents/2017/"
in_file_format = "gcf"
in_file_extension = "gcf"
out_file_format = "mseed"
# Input "1" to extract seismogram parameters from file name. For
# everything else the parameters will be extracted from the header.
extract_params_fname = "1"

class SeisFile(object):
    """Seismogram file class."""

    seis_files = []

    def __init__(self, file_path, file_ext=in_file_extension):
        split_path = list(filter(None, file_path.split('/')))
        fext_len = len(file_ext)
        self.seis_files.append(self)
        self.fpath = file_path
        self.fname = split_path[-1]
        self.fext = file_ext

        if fext_len > 0:
            fext_slice = -1 - fext_len
            fpath_trun = self.fpath[:fext_slice]
            fname_trun = self.fname[:fext_slice]
            self.fpath_trun = fpath_trun
            self.fname_trun = fname_trun
        else:
            self.fpath_trun = self.fpath
            self.fname_trun = self.fname
    
    def extract_params_CRO(self, fname_separ='_'):
        """Extracts parameters from input seismogram file name if data
        provided in header is not correct. Input file name in this case
        is of form:
            STAT_C_SRT_YYYYMMDD_HHMM, where
                STAT - station ID/name,
                C - seismogram component,
                SRT - sample rate,
                YYYYMMDD - date,
                    YYYY - year,
                    MM - month,
                    DD - day,
                HHMM - start time of the seismogram,
                    HH - hours,
                    MM - minutes."""
        file_params = list(filter(None, self.fname_trun.split(fname_separ)))
        self.network = "CR"
        self.station = file_params[0].upper()
        self.component = file_params[1].upper()
        self.sample_rate = int(file_params[2])
        self.date = file_params[3]
        self.starttime = file_params[4]

        if 50 <= self.sample_rate and self.sample_rate < 100:
            self.channel = f"BH{self.component}"
        elif self.sample_rate >= 100:
            self.channel = f"HH{self.component}"
        else:
            self.channel = f"LH{self.component}"

    def format_output(self, output_format=out_file_format):
        self.outf = output_format
        self.fout = f"{self.fpath_trun}.{output_format}"


file_paths = []

for root, dirs, files in os.walk(input_file_folder):
    ext_len = -len(in_file_extension)
    for file_name in files:
        file_ext = file_name[ext_len:]
        # Skip files with inappropriate extension.
        if file_ext == in_file_extension:
            file_path = path.join(root, file_name)
            file_paths.append(file_path)
        else:
            continue

for file_pathi, file_path in enumerate(file_paths):
    seis_file = SeisFile(file_path, in_file_format)
    st = read(seis_file.fpath)
    print('INPUT FILE {}/{}: {}'.format(
        file_pathi + 1, len(file_paths), seis_file.fpath
    ))

    if extract_params_fname == "1":
        seis_file.extract_params_CRO()
        for tr in st:
            tr.stats.network = seis_file.network
            tr.stats.station = seis_file.station
            tr.stats.channel = seis_file.channel
    else:
        pass

    seis_file.format_output()
    st.write(seis_file.fout, format=seis_file.outf)
    print('OUTPUT FILE {}/{}: {}'.format(
        file_pathi + 1, len(file_paths), seis_file.fout
    ))

print('\nDONE!\n')

end_time = time.clock()

duration = end_time - start_time

print('Running time: {:.2f} s.\n'.format(duration))

# all_files = seis_file.seis_files