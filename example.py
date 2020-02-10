#-*- coding: utf-8 -*-

import obseis_convert as osc


ROOT_FOLDER = "/path/to/root/folder/"
IN_FILE_FORMAT = "sac"
IN_FILE_EXTENSION = "SAC"
OUT_FILE_FORMAT = "mseed"

EXTRACT_PARAMS_FNAME = 2
CREATE_NEW_ROOT = True

sfs = osc.SeisFiles(
    ROOT_FOLDER, IN_FILE_EXTENSION, IN_FILE_FORMAT,
    OUT_FILE_FORMAT, new_root=CREATE_NEW_ROOT,
    extract_params_fname=EXTRACT_PARAMS_FNAME
    )
sfs.convert_files()

