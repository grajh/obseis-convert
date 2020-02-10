#-*- coding: utf-8 -*-

#**********************************************************************
# Script name: obseis_convert.py
# Version: 2020.02.07
# Description: Python script for converting seismograms between file
#   formats supported by ObsPy.
#
# Author: Gregor Rajh
# Year: 2020
# Python version: 3
# Requirements:
#   *obspy and its dependencies
#
# e-mail: rajhgregor@gmail.com
#**********************************************************************

import os
import time

import obspy
from obspy import read


def folder_check(save_path):
    """Create folders necessary for given path.
    
    Arguments:
        save_path {string}
    """
    try:
        os.makedirs(save_path)
    except OSError:
        if not os.path.isdir(save_path):
            raise

class SeisFile(object):
    """Seismogram file class. Holds information about each input file
    and has three methods."""

    def __init__(self, file_path, file_path_out, file_ext, in_format,
       out_format, extract_params_fname, fname_separator='_'):
        # Split file name and path.
        split_path = os.path.split(file_path)
        split_path_out = os.path.split(file_path_out)
        # Write function arguments.
        self.fpath = file_path
        self.fpath_out = file_path_out
        self.fname = split_path[1]
        self.fname_out = split_path_out[1]
        self.fext = file_ext

        # Format check.
        if in_format:
            self.in_format = in_format.upper()
        else:
            self.in_format = None

        if out_format:
            self.out_format = out_format.upper()
        else:
            # If no output format is provided, save to mseed.
            self.out_format = 'MSEED'

        self.extract_params_fname = extract_params_fname
        self.fname_separ = fname_separator

        # Split extension and file name.
        fpath_trun = os.path.splitext(self.fpath)[0]
        fname_trun = os.path.splitext(self.fname)[0]
        self.fpath_trun = fpath_trun
        self.fname_trun = fname_trun
        fpath_trun_out = os.path.splitext(self.fpath_out)[0]
        fname_trun_out = os.path.splitext(self.fname_out)[0]
        self.fpath_trun_out = fpath_trun_out
        self.fname_trun_out = fname_trun_out

        # Format output file name.
        self.fout = f"{self.fpath_trun_out}.{out_format}"

    def extract_params_from_name(self):
        """Extracts parameters from input seismogram file name if data
        provided in header is not correct. Input file name provided
        under 'self.fname_trun' variable and in the case of option
        number 1 is of form:
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
                    MM - minutes.
        """

        if self.extract_params_fname == 1:
            file_params = list(filter(
                None, self.fname_trun.split(self.fname_separ)))
            self.network = "CR"
            self.station = file_params[0].upper()
            self.component = file_params[1].upper()
            self.sample_rate = int(file_params[2])
            # self.date = file_params[3]
            # self.starttime = file_params[4]

            if 10 <= self.sample_rate < 80:
                self.channel = f"BH{self.component}"
            elif self.sample_rate >= 80:
                self.channel = f"HH{self.component}"
            else:
                self.channel = f"LH{self.component}"

        elif self.extract_params_fname == 2:
            file_params = list(filter(
                None, self.fname_trun.split(self.fname_separ)))
            self.network = "CR"
            self.station = file_params[0].upper()
            self.channel = file_params[2].upper()
            # self.date = file_params[:8]
            # self.starttime = file_params[8:]

    def read_file(self):
        """Parse file content to Obspy stream object and update basic
        parameters based on file name if appropriate choice is given.
        """

        try:
            self.st = read(self.fpath, format=self.in_format)

            if self.extract_params_fname in [1, 2]:
                self.extract_params_from_name()

                for tr in self.st:
                    tr.stats.network = self.network
                    tr.stats.station = self.station
                    tr.stats.channel = self.channel
            else:
                pass

        # TypeError. If format is not in format list.
        except Exception as e:
            print(e)

    def write_file(self):
        """Write stream object to specified format."""

        self.st.write(self.fout, format=self.out_format)


class SeisFiles(object):
    """Class holding all SeisFile objects."""

    def __init__(self, in_folder, in_ext, in_format, out_format,
       new_root=True, extract_params_fname=0, fname_separator='_'):
        self.in_folder = in_folder
        self.in_ext = in_ext

        if in_format:
            self.in_format = in_format.upper()
        else:
            self.in_format = None

        if out_format:
            self.out_format = out_format.upper()
        else:
            self.out_format = 'MSEED'

        self.new_root = new_root
        self.extract_params_fname = extract_params_fname
        self.fname_separ = fname_separator
        self.seis_files = []

        if self.new_root:
            if self.in_folder.endswith('/'):
                    self.in_folder = self.in_folder[:-1]
            else:
                pass

            self.out_folder = self.in_folder + '_converted'

        else:
            self.out_folder = self.in_folder

        self.file_paths = []
        self.file_paths_out = []

        for root, _, files in os.walk(self.in_folder):

            if self.new_root:
                root_out = root.replace(self.in_folder, self.out_folder)
            else:
                root_out = root

            self.root_out = root_out

            for file_name in files:
                file_ext = os.path.splitext(file_name)[1][1:]

                # Skip files with different extension.
                if self.in_ext and file_ext == self.in_ext:
                    file_path = os.path.join(root, file_name)
                    file_path_out = os.path.join(root_out, file_name)
                    self.file_paths.append(file_path)
                    self.file_paths_out.append(file_path_out)
                elif not self.in_ext:
                    file_path = os.path.join(root, file_name)
                    file_path_out = os.path.join(root_out, file_name)
                    self.file_paths.append(file_path)
                    self.file_paths_out.append(file_path_out)
                else:
                    continue

                # Create 'SeisFile' object for each file found
                # recursively in root folder.
                seis_file = SeisFile(file_path, file_path_out, self.in_ext,
                    self.in_format, self.out_format,
                    self.extract_params_fname, self.fname_separ)
                self.seis_files.append(seis_file)

    def convert_files(self, verbose=False):
        start_time = time.perf_counter()
        print('\nSeismograms input folder: {}.'.format(
            os.path.join(self.in_folder, '*')))
        print('Saving to: {}.'.format(os.path.join(self.out_folder, '*')))
        print('Converting from {} to {} format.\n'.format(
            self.in_format, self.out_format))

        for sfi, seis_file in enumerate(self.seis_files, 1):
            seis_file.read_file()

            if verbose:
                print('INPUT FILE {}/{}: {}'.format(
                    sfi, len(self.seis_files), seis_file.fpath
                ))

            folder_check(os.path.dirname(seis_file.fpath_out))

            seis_file.write_file()

            if verbose:
                print('OUTPUT FILE {}/{}: {}\n'.format(
                    sfi, len(self.seis_files), seis_file.fout
                ))
            else:
                percent_val = (sfi / float(len(self.seis_files))) * 100
                print('Convert progress: {:.0f} %. |{}{}|\r'.format(
                    percent_val, '*' * int(percent_val / 2),
                    ' ' * (50 - int(percent_val / 2))), end='\r', flush=True)

        print('\n\nDONE!\n')

        end_time = time.perf_counter()

        duration = end_time - start_time

        print('Running time: {:.2f} s.\n'.format(duration))

