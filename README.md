## obseis-convert
A convenient Python script for converting seismograms between file formats supported by ObsPy. Also supports extracting basic seismogram parameters from a filename, based on an input template. Works in Python 3. An end user only has to define input folder, input file format, input file extension and output file format. The script recursively searches the input folder for files with the specified file extension. Seismogram parameters written in the filename can be extracted and written into the output file. In this case the user has to provide a template in a specified form. Script can write new seismogram files with the same name but different extension in the same folder as input files or create a new root folder with the same tree structure. Progress bar is shown by default. Verbose mode is also available through 'verbose' parameter of 'convert_files' method in 'SeisFiles' class.

Dependencies:
- [Obspy](https://github.com/obspy/obspy/wiki)

Obspy is a Python toolbox for seismology.
More information about the Obspy project can be found [here](https://github.com/obspy/obspy/wiki).

Updates:  
Major update. Improved and cleaned.
Next step add an example to README, document the script better.

Last update: 10. February 2020.
