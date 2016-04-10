import sys
import os

#  This script adds a number of Gaussians to the initialized Hidden Markov Models. 
#  This will be either the whole HMM (if single-state) or the emission function.
#  The input arguments are:
#    1. name of the command file for HHEd
#    2. list of the models

# Initialisation
numStates = raw_input("Enter number of states in model as a word ('One', 'Two'): ")
vectorType = raw_input("Enter type of vector features are derived from (e.g. 'MFCC' or 'LPC'): ")

# Convert arguments to upper-case if they are not:
if not (vectorType.isupper()):
	vectorType = vectorType.upper()
if not (numStates[0].isupper()):
	numStates = numStates[0].upper() + numStates[1:]
	

# Definition of paths
modelPath = numStates + "State/" + vectorType + "/"
rootDirectory = "F:/Accommodation/Files/"
initializedModelsPath = rootDirectory + "5.Models/initializedModels/" + modelPath
mixtureModelsPath = rootDirectory + "5.Models/mixtureModels/" + modelPath
modelsListName = rootDirectory + "Lists/modelsList.txt"							# Note: all lines in the model file must have a newline appended. 
commandFileName = rootDirectory + "Lists/hhedCommandFile"

# Configuration variables.
configurationFileName = "configparameters.cfg"
varianceFloor = "0.000001"
verbosityLevel = "00001"
iterationsNumber = 10


# Initialization of the models (computation of means and variances)
command = "HHEd"
command = command+" -M " +mixtureModelsPath 			# directory of the mixture models
command = command+" -T " +verbosityLevel

modelsFileIn = open(modelsListName,'r')
models = modelsFileIn.readlines()
modelsFileIn.close()

for item in models:
	command = command+ " -H " + initializedModelsPath + item[:len(item)-1] +" "

command = command+ " " + commandFileName 		
command = command+ " " + modelsListName

print command
os.system(command)


