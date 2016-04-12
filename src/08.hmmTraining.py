import sys
import os

# This script trains Hidden Markov Models through the expectation-maximisation algorithm
# Baum-Welch re-estimation. 
#  Input arguments are:
# 	1. name of the speaker (the code of the speaker)
# 	2. name of the training set
# 	3. list of the models

# Initialization. Arguments are used in file paths, so must be exact.
numStates = raw_input("Enter number of states in model as a word ('One', 'Two'): ")
vectorType = raw_input("Enter type of vector to train on (e.g. 'MFCC' or 'LPC'): ")

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
rootDirectory = "F:/Accommodation/Files/"
labelFilesPath = rootDirectory + "4.Labels/speakerLabels"
trainedModelsPath = rootDirectory + "5.Models/trainedModels/" + modelPath
trainingDataPath = rootDirectory + "Lists/TrainingDataLists/" + vectorType + "/"
mixtureModelsPath = rootDirectory+ "5.Models/mixtureModels/" + modelPath
modelsListFileName = rootDirectory + "/Lists/modelsList.txt"

# Config variables. Standard file plus Model levels.
varianceFloor = "0.000001"
verbosityLevel = "00001"
iterationsNumber = 10


# For each speaker:
for index in range(len(speakerArray)):

	speakerName = speakerArray[index]
	trainingListFilePath = trainingDataPath + speakerName + "trainingset.txt"

	# Train the model until the parameters (repeat of embedded Baum-Welch re-estimation)
	for k in range(1, iterationsNumber+1):
		print speakerName, "training iteration #", k

		command = "HERest"
		command = command+" -S "+ trainingListFilePath 				#  List of training files
		command = command+" -M "+ trainedModelsPath+ "iter"+str(k)  #  Output directory
		command = command+" -L "+ labelFilesPath 					#  Label files directory
			
		command = command+" -d "+ mixtureModelsPath					#  Sets mixture models as the HMM
		command = command+" -v "+ varianceFloor 					#  Setting the variance floor
		command = command+" -T "+ verbosityLevel
		
		command = command+" " + modelsListFileName 					# List of models
		
		os.system(command)
