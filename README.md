## obseis-convert
A convenient Python script for converting seismograms between file formats supported by ObsPy. Also supports extracting basic seismogram parameters from a filename, based on an input template. Works in Python 3. An end user only has to define input folder, input file format, input file extension and output file format. The script recursively searches the input folder for files with the specified file extension. Seismogram parameters written in the filename can be extracted and written into the output file. In this case the user has to provide a template in a specified form. Script can write new seismogram files with the same name but different extension in the same folder as input files or create a new root folder with the same tree structure. Progress bar is shown by default. Verbose mode is also available through 'verbose' parameter of 'convert_files' method in 'SeisFiles' class.

Dependencies:
- [Obspy](https://github.com/obspy/obspy/wiki)

Obspy is a Python toolbox for seismology.
More information about the Obspy project can be found [here](https://github.com/obspy/obspy/wiki).

Example:

```
# Import the module.
import obseis_convert as osc

# Define user parameters.
ROOT_FOLDER = "/path/to/root/folder/"
# File format of input files.
IN_FILE_FORMAT = "sac"
# File extension of input files.
# Use empty string or None to go through all files.
IN_FILE_EXTENSION = "SAC"
# Desired output format. If not specified, mseed is used by default.
OUT_FILE_FORMAT = "mseed"

# Parameter for extracting parameters from file name.
# Input 0 to extract parameters from header.
# Currently two templates (options 1 and 2) are implemented for
# extracting parameters. Modify them to you needs in
# 'extract_params_from_name' method of 'SeisFile' class.
EXTRACT_PARAMS_FNAME = 2
# Specifiy separator between parameters in file name.
# Can be overridden in a template.
FNAME_SEPARATOR = '_'

# If set to True it creates new folder for converted seismograms with
# the same internal tree structure.
CREATE_NEW_ROOT = True

# Create SeisFiles object, holding information about all files
# available. Root folder is read on initialization of the object.
sfs = osc.SeisFiles(
    ROOT_FOLDER, IN_FILE_EXTENSION, IN_FILE_FORMAT,
    OUT_FILE_FORMAT, new_root=CREATE_NEW_ROOT,
    extract_params_fname=EXTRACT_PARAMS_FNAME,
    fname_separator=FNAME_SEPARATOR
    )

# Call convert files method and wait ... DONE!
sfs.convert_files()
```

Updates:
Major update. Improved and cleaned. Added an example.

Next steps:
    Include more comments in the script.
    Wildcards for filenames (fnmatch) and/or seismogram parameters.

Last update: 10. February 2020.
