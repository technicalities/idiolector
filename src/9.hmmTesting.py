import sys
import os

#  This script tests Hidden Markov Models by recognising models with their own or target MFCs. ('Recogniser evaluation')
#  This yields a series of recognition files (containing the probability of the word given the model).

# The input arguments are:
# 	1) the number of states in the model
#	2) the type of feature to use
#	3) whether to recognise with own model ("self") or pair's model ("target").

#  The outputs are transcriptions, "rec" files in the format
#  [start] [end] [speaker[state]] [log likelihood] [pronounication]


# Command line initialisation		
numStates = raw_input("Enter number of states in model as a word ('One', 'Two'): ")									
vectorType = raw_input("Enter type of vector to create labels for (e.g. 'MFCC' or 'LPC'): ")

# Convert arguments to upper-case if they are not:
if not (vectorType.isupper()):																
	vectorType = vectorType.upper()															
if not (numStates[0].isupper()):															
	numStates = numStates[0].upper() + numStates[1:]										


# Definition of paths
modelPath = numStates + "State/" + vectorType + "/"
rootDirectory = "F:/Accommodation/Files/"
trainedModelsPath = rootDirectory + "5.Models/trainedModels/" + modelPath
trainedModelsName = trainedModelsPath + "/iter10/newMacros" 						#  The location of the models after all training iterations and mixing.				
testPath = rootDirectory + "Lists/TestDataLists/" + vectorType +"/"									
dictionaryPath = rootDirectory+ "Lists/Dictionaries/" + numStates + "State/"										
syntaxPath = rootDirectory+ "Lists/Syntax/"													
grammarPath = rootDirectory+ "Lists/Grammars/"												
recognitionPath = rootDirectory + "6.Recognitions/" + modelPath 					#  Output directory.

# Config variables.
varianceFloor = "0.000001"
verbosityLevel = "00004"

speakerArray = ["ARA14", "GJN14", "HLH30", "JSE11",
				"JTN20", "JYN22", "KBN30", "SCA01", 
				"SHA13", "SKN03", "TMY30", "ZSE07"]		

				
# Loop performs HParse and HVite decoding for each of our twelve models:
for index in range(len(speakerArray)):

	speakerCode = speakerArray[index]												#  The speaker model to test.							
	modelsListName = rootDirectory + "Lists/SpeakerPairs/" + speakerCode + ".txt"	#  File containing chosen speaker and their paired speaker.
	syntaxName = syntaxPath + speakerCode + "Syntax.txt" 							#  Generated schema of speaker
	dictionaryName = dictionaryPath + speakerCode + "Dictionary.txt"

#  Whether model is tested against own or other's data.								#  If producing recognitions conditional on own model, 
	selfDataName = testPath + speakerCode + "testset.txt"							#  Simply append own speakerCode (use own test set).
																					
	modelsFileIn = open(modelsListName,'r')											#  Else for producing recognitions against paired model,
	models = modelsFileIn.readlines()												#  Lookup the paired speaker code.
	modelsFileIn.close()			
	pairCode = models[1]															#  Pair's code is second in the list.
	testListName = testPath + pairCode + "testset.txt"								#  Then use test data from paired speaker.
	
	
# A Viterbi word-recogniser. Evaluates the model and outputs log probabilities log p(Xi | Oa).
	print "HVite"
	
	print "Testing " + speakerCode + " against " + pairCode + "'s data"
	
	command = "HVite"
	command = command+" -w " + syntaxName 					#  Setting the syntax
	command = command+" -S " + testListName 				#  List of test files to use
	command = command+" -l " + recognitionPath + "self"	 	#  Set the output directory of recognitions
	command = command+" -H " + trainedModelsName 			#  Input model to test
	command = command+" -f "								#  Track the full state alignment

	command = command+ " " + dictionaryName					#  The dictionary: speaker model and monophone of same speaker code.
	command = command+ " " + modelsListName 				#  List of models
	os.system(command)
	
	
	print "Testing " + speakerCode + " against own data"
	
	command = "HVite"
	command = command+" -w " + syntaxName 					#  Setting the syntax
	command = command+" -S " + selfDataName 				#  List of test files to use
	command = command+" -l " + recognitionPath + "target"	#  Set the output directory of recognitions
	command = command+" -H " + trainedModelsName 			#  Input model to test
	command = command+" -f "								#  Track the full state alignment

	command = command+ " " + dictionaryName					#  The dictionary: speaker model and monophone of same speaker code.
	command = command+ " " + modelsListName 				#  List of models

	os.system(command)
	
	print "Completed computing recognitions for", speakerCode
	
