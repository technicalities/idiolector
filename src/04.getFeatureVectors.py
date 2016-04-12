import sys
import os
# This script extracts the chosen type and order of features from the .wav files.

# The input parameters are:
# 1) a configuration file detailing vector type, order, and windowing constants.
# 2) a script file
# 3) Trace flags level, verbosity
# 4) Output path

# The outputs are one vector representation for each input waveform.


# Initialization
vectorType = raw_input("Enter type of vector to extract from audio (e.g. 'MFCC' or 'LPC'): ")

# Convert arguments to upper-case if they are not:
if not (vectorType.isupper()):
	vectorType = vectorType.upper()

	
# Definition of paths
rootDirectory = "F:/Accommodation/Files/"
configurationFilePath = rootDirectory + "Lists/Config/"
vectorFilesPath = rootDirectory+ "3.Vectors/" + vectorType + "s/"
wavFilesPath = rootDirectory + "2.WavWords/"
scpFileName = rootDirectory + "Lists/VectorLists/" + vectorType + "scpList.txt"

# Configuration
configurationFileName = configurationFilePath + vectorType + "configparameters.cfg"
verbosityLevel = "00002"

print "Script file used is " + scpFileName
print "Output directory is " + vectorFilesPath


# Extract feature vectors from waveforms. HCopy used as a speech coding tool.
command = "HCopy"

if (vectorType == "MFCC") :
	command = command+" -l "+ vectorFilesPath 						# Setting output directory.
command = command+" -C "+ configurationFileName 					# Setting the configuration.
command = command+" -S "+ scpFileName 								# set script file listing all source and target files' paths.
command = command+" -T "+ verbosityLevel 							# Set level of trace to a line by line report.

os.system(command)

print "Script complete."


