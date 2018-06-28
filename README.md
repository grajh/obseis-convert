## obseis-convert
A convenient Python script for converting seismograms between file formats supported by ObsPy. Also supports extracting seismogram parameters from a filename, based on an input template. Works in both Python 2 and 3. An end user only has to define input folder, input file format, input file extension and output file format. The script reads only those files in the input folder with the specified file extension. Seismogram parameters written in the filename can be extracted and written into the output file. In this case the user has to provide a template in a specified form. Currently the script writes new seismogram files with the same name but different extension in the same folder as input files.

Dependencies:
- [Obspy](https://github.com/obspy/obspy/wiki)

Obspy is a Python toolbox for seismology.
More information about the Obspy project can be found [here](https://github.com/obspy/obspy/wiki).

Updates:  
Initial upload done.
Next step is to generalize some procedures, include some examples and document the script better.

Last update: 28. June 2018.
