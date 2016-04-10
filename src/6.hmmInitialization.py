import sys
import os
#  This script initialises all speaker's root hidden Markov models. 
#  It is a 'flat' initialisation (each state set to same initial values) 
#  before the training process at script #8.

#  Input arguments are:
# 	 1. number of states
# 	 3. list of the models


# Initialization: all 12 speaker codes.
numStates = raw_input("Enter number of states in model as a word ('One', 'Two'): ")
vectorType = raw_input("Enter the vector type of the training data (e.g. 'MFCC' or 'LPC'): ")

# Convert arguments to upper-case if they are not:
if not (vectorType.isupper()):
	vectorType = vectorType.upper()
if not (numStates[0].isupper()):
	numStates = numStates[0].upper() + numStates[1:]


speakerArray = ["ARA14", "GJN14", "HLH30", "JSE11", 
				"JTN20", "JYN22", "KBN30", "SCA01",
				"SHA13", "SKN03", "TMY30", "ZSE07"]
				

# Definition of paths
modelPath = numStates + "State/" + vectorType + "/"
labelFolder = "4.Labels/speakerLabels/"
rootFolder = "5.Models/rootModels/" + modelPath
initFolder = "5.Models/initializedModels/" + modelPath
trainedFolder = "5.Models/trainedModels/"+ modelPath

rootDirectory ="F:/Accommodation/Files/"
rootModelsPath = rootDirectory + rootFolder
initializedModelsPath = rootDirectory + initFolder
trainedModelsPath = rootDirectory + trainedFolder
labelFilesPath = rootDirectory + labelFolder
trainingDataPath = rootDirectory + "Lists/TrainingDataLists/" + vectorType + "/"

# Config variables.
varianceFloor = "0.000001"
verbosityLevel = "00001"


# Initialization of the models (computation of means and variances)
for index in range(len(speakerArray)):

	speakerName = speakerArray[index]
	trainingListFilePath = trainingDataPath + speakerName + "trainingset.txt"
	command = "HCompV"
	command += " -S " + trainingListFilePath 		# List of training files
	command = command+" -M " +initializedModelsPath # Output directory
	command = command+" -L " +labelFilesPath 		# Label files directory
	command = command+" -m" 						# Flag to compute both means AND covariances
	command = command+" -l "+ speakerName 			# Segment label the model accounts for
	command = command+" -v "+ varianceFloor 		# Setting the variance floor
	command = command+" -o "+ speakerName 			# Setting the name of the output model
	command = command+" -T "+ verbosityLevel

	command = command + " "+ rootModelsPath + speakerName 		# Name of model structure file
	os.system(command)
	print "Completed initialising", speakerName