import os
import sys
import csv
import scipy.stats

# A script unifying all the scripts, calling the HTK tools in sequence with the appropriate file paths:
# this takes us from wav files segmented by word, to 132 speaker-pair likelihood-ratio correlations. 

# Stages:
# 1. getFeatureVectors.py - creates vectors from .wav files
# 2. getLabelsFromVectors.py - derives labels from the vector files
# 3. hmmInitialization.py - one model per speaker, sets means and variances.
# 4. hmmAddingGaussians.py - multiplying the number of Gaussians for each model.
# 5. hmmTraining.py - training the models by embedded re-estimation
# 6. getLattice - parse the task grammar and verify the model syntax.
# 7. hmmTesting.py - .
# 8. getAccommodation.py - calculates all log likelihood ratios for words from paired speakers.
# 9. getCorrelations.py - calculates the correlation of the ratios.


#  The codes of all the speaker models:
speakerArray = ["ARA14"]#, "GJN14", "HLH30", "JSE11", 
				#"JTN20", "JYN22", "KBN30", "SCA01",
				#"SHA13", "SKN03", "TMY30", "ZSE07"]

				
# Set modelling parameters by command prompt:
vectorType = raw_input("Enter type of vector used in this analysis (e.g. 'MFCC' or 'LPC'): ")
numStates = raw_input("Enter number of states in model as a word ('One', 'Two'): ")

# Validate the input
if not (vectorType.isupper()):
	vectorType = vectorType.upper()
if not (numStates[0].isupper()):
	numStates = numStates[0].upper() + numStates[1:]
	
	
#############################################################################################################################################

	# Definition of common paths:
	
rootDirectory = "F:/Accommodation/Files/"

configurationFilePath = rootDirectory + "Lists/Config/"								# Location of feature extraction settings files.
wavFilesPath = rootDirectory + "2.WavWords/"										# Directory of source waveforms.	
vectorFilesPath = rootDirectory+ "3.Vectors/" + vectorType + "s/"					# Directory of source vector files.									
labelFilesPath = rootDirectory + "4.Labels/speakerLabels/"							# Directory of label files.

	# General configuration variables.
varianceFloor = "0.000001"
verbosityLevel = "00001"
configurationFileName = configurationFilePath + vectorType + "configparameters.cfg"


#############################################################################################################################################

# 6. hmmInitialization.py - takes the model prototypes and yields flat-start models.

#  This script initialises all speakers' prototype hidden Markov models. 
#  It is a 'flat' initialisation (each state set to same initial values) before the training process at script #5.

os.system("06.hmmInitialization.py 1")
# Model paths:
modelPath = numStates + "State/" + vectorType + "/"
rootModelsPath = rootDirectory + "5.Models/rootModels/" + modelPath
initializedModelsPath = rootDirectory + "5.Models/initializedModels/" + modelPath
mixtureModelsPath = rootDirectory + "5.Models/mixtureModels/" + modelPath
trainedModelsPath = rootDirectory + "5.Models/trainedModels/" + modelPath
trainedModelsName = trainedModelsPath + "/iter10/newMacros" 						#  The location of the models after all training iterations and mixing.				

trainingDataPath = rootDirectory + "Lists/TrainingDataLists/" + vectorType + "/"
testPath = rootDirectory + "Lists/TestDataLists/" + vectorType +"/"	


# Initialization of the models (computation of global means and variances for GMM components).
for index in range(len(speakerArray)):

	speakerName = speakerArray[index]
	trainingListFilePath = trainingDataPath + speakerName + "trainingset.txt"
	
	command = "HCompV"
	command += " -S " + trainingListFilePath 					# List of training files
	command = command+" -M " +initializedModelsPath 			# Output directory
	command = command+" -L " +labelFilesPath 					# Label files directory
	command = command+" -m" 									# Flag to compute both means AND covariances
	command = command+" -l "+ speakerName 						# Segment label the model accounts for
	command = command+" -v "+ varianceFloor 					# Setting the variance floor
	command = command+" -o "+ speakerName 						# Setting the name of the output model
	command = command+" -T "+ verbosityLevel

	command = command + " "+ rootModelsPath + speakerName 		# Name of model structure file
	os.system(command)
	print "Completed initialising", speakerName

	
	
#############################################################################################################################################

# 4. hmmAddingGaussians.py - multiplying the number of Gaussians for each model.

#  This script adds a number of Gaussians to the initialized Hidden Markov Models. 
#  This will be either the whole HMM (if single-state) or the emission function of each state.

#  The input arguments are:
#    1. name of the command file for HHEd
#    2. list of the models

#  Paths:					
modelsListName = rootDirectory + "Lists/modelsList.txt"								#  Note: all lines in the model file must have a newline appended. 					
commandFileName = rootDirectory + "Lists/hhedCommandFile"		

#  Initialization of the models (computation of means and variances)
command = "HHEd"
command = command+" -M " +mixtureModelsPath 					# directory of the mixture models
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


		
#############################################################################################################################################

# 5. hmmTraining.py - training the models by embedded re-estimation

#   This script trains Hidden Markov Models through the expectation-maximisation algorithm, Baum-Welch re-estimation. 
#   Input arguments are:
#   	1. name of the speaker (the code of the speaker)
# 	    2. name of the training set
# 	    3. list of the models
#       4. number of iterations of Baum-Welch estimation to perform.


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
		
		command = command+" " + modelsListName 						# List of models
		
		os.system(command)

		

#############################################################################################################################################

		# 6. getLattice - parse the task grammar and verify the model syntax.

# This script builds a word-recognition network from the Backus-Naur grammar.
# In our case, it is a very simple lattice, involving one 'word' (the speaker model).

# The input arguments are:
# 	1) a speaker's code
#	2) the corresponding simple BN grammar file path.

#  The outputs are "Syntax" files in the format [speakercode]Syntax.txt.		


#  File paths:
syntaxPath = rootDirectory+ "Lists/Syntax/"													
grammarPath = rootDirectory+ "Lists/Grammars/"	
dictionaryPath = rootDirectory+ "Lists/Dictionaries/" + numStates + "State/"										


for index in range(len(speakerArray)):

	speakerCode = speakerArray[index]														#  The speaker model to test.							
	grammarName = grammarPath + speakerCode + "Grammar.txt"
	syntaxName = syntaxPath + speakerCode + "Syntax.txt" 									#  Generated schema of speaker

	
# Parses the Backus-Naur grammar ('grammar') into a word network ('syntax')
	print "HParse",">>>>>"
	command = "HParse"
	command = command+" "+ grammarName
	command = command+" "+ syntaxName
	command = command+" -T "+ verbosityLevel
	
	os.system(command)
		
		
#############################################################################################################################################

		# 7. hmmTesting.py - .

#  This script tests Hidden Markov Models by recognising models with their own or target MFCs. ('Recogniser evaluation')
#  This yields a series of recognition files (containing the probability of the word given the model).

# The input arguments are:
# 	1) the number of states in the model
#	2) the type of feature to use
#	3) whether to recognise with own model ("self") or pair's model ("target").

#  The outputs are transcriptions, "rec" files in the format
#  [start] [end] [speaker[state]] [log likelihood] [pronounication]
			

#  Paths:
recognitionPath = rootDirectory + "6.Recognitions/" + modelPath 					#  Output directory.
recognitionListPath = rootDirectory + "Lists/RecognitionLists/" + modelPath
			
				
# Loop performs HVite recognition for each word of our twelve speakers:
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
	
	
# A speaker recogniser. Evaluates the model and outputs log probabilities, log p(word | model).
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
		
		
#############################################################################################################################################
	
		# 8. getAccommodation.py - calculates all log likelihood ratios for words from paired speakers.

#  This script calculates the logarithm of the ratio p(x_A|A)/p(x_A|B) for each word.
#  The first prob p(x_A|B) is from tbe "Recognitions/target". It is the probability of x_A being produced by model B. 
#  The second probability p(x_A|A) is the probability of x_A being produced by model A (it is in directory Recognitions/self).

#  The input parameters are: 
#     1) a list of 'target' .rec files (a txt file of path-names),

#  The output is one .csv file per speaker, listing, for each rec file: 
#    1) file path, 2) the time, 3) the log likelihood ratio, 4) the word, 5) word length in chars, 6) frame number extracted at.


# For each speaker:
for index in range(len(speakerArray)):

	speakerCode = speakerArray[index]
	recListPath = recognitionListPath + speakerCode + "recs.txt"
	# The CSV file to write transcriptions to.
	outputFile = rootDirectory + "7.Outputs/Accommodations/" + modelPath + speakerCode + "accomm.csv" 	

	# Reading the list of rec files
	recListFile = open(recListPath,'r')
	targetRecList = recListFile.readlines()
	recListFile.close()

	count = 0

	# Redirect standard output stream:
	old_sysout = sys.stdout														# Store output stream in temp
	outFile = open(outputFile, 'w')												# New file.
	sys.stdout = outFile														# Redirect print commands to outFile.

	# For each recognition file in the 'target' directory:
	for itemTarget in targetRecList:
		# Getting the name of the rec files
		itemTarget = itemTarget[0:len(itemTarget)-1]							# Pathname of current target rec file.
		itemSelf = itemTarget.replace("target", "self",1)						# Create a path to the equivalent 'self' recognition file.
		
		# Extracting the time from the rec file name
		itemNameList = itemTarget.split('-')									# Produces an Array of: [0] path + task_speaker; [1] word spoken; [2] the time
		timeList = itemNameList[len(itemNameList)-1].split('.')					# Array of: [0] secs time, [1] millisecs time, and [2] ".rec"
		time = float(timeList[0]) + float(timeList[1]) * 0.001					# Divide by 1000 to obtain time
		word = itemNameList[1]
		
		# Extracting the target likelihood
		recFile = open(itemTarget,'r')									
		rec = recFile.readline()
		recFile.close()
		targetLikelihood = float(rec.split()[3])								#  Assign the log likelihood
		frameNumber = float(rec.split()[1])*0.00001								#  Find the frame it was spoken at (division by 10,000).
		
		# Extracting the self likelihood
		recFile = open(itemSelf,'r')
		rec = recFile.readline()
		recFile.close()
		selfLikelihood = float(rec.split()[3])
		itemTargetList = itemTarget.split('/')
		
		ratio = selfLikelihood - targetLikelihood								# Subtracting the logs gives us our A/B ratio.
		
		# Output to CSV in format: [Rec file path, log-likelihood ratio, word spoken, length of word, frame extracted at].
		print itemTargetList[len(itemTargetList)-1],",",time,",",ratio,",",word,",",len(word),",",frameNumber
		
		count = count + 1

		
	sys.stdout = old_sysout
	outFile.close()
	print "Completed computing", count, "likelihoods for", speakerCode		
		

#############################################################################################################################################
		
		# 9. getCorrelations.py - calculates the correlation of the ratios.

#  This program plots the accommodation data and derives a correlation from the point likelihood ratios over time.

#  Inputs are one .csv file per speaker, listing the log-likelihood ratio for each of their words.
#  Output is one csv file summarising the correlation between log-likelihood and time, for each analysis unit (speaker i on task j).

		
#  Path names.
taskPath = rootDirectory + "Lists/TestDataLists/TestTasks/"
accommPath = rootDirectory + "7.Outputs/Accommodations/" + modelPath + "/"
outputFile = rootDirectory + "7.Outputs/Correlations/" + modelPath + "rawOutputTest.csv" 		

counterPositive = 0																# Counter for the total no. of positive correlations.
			
			
# Redirect standard output stream to a csv:
old_sysout = sys.stdout															# Store the output stream in a temp variable.
outFile = open(outputFile, 'w')													# Create the new 'rawOutput' file.
sys.stdout = outFile															# Redirect following print commands to the outFile.


# Set up a table format for the output file. Column headers:
print "Speaker-task",",","Correlation coefficient",",""Absolute rho",",","P-value",",","Max time"
	
#  Loop finds the correlations for each task of of our twelve models:
for index in range(len(speakerArray)):

	speakerCode = speakerArray[index]											#  The speaker model to infer from.	
	accommodationFileName = accommPath + speakerCode + "accomm.csv" 
	taskFile = taskPath + speakerCode + "tasks.txt"
	
	taskFileIn = open(taskFile,'r')												#  Read in a list of the 11 test tasks.
	tasks = taskFileIn.readlines()
	taskFileIn.close()	

	for task in tasks:
		taskName = task[0:len(task)-1]											#  Truncate the delimiter (e.g. "raB_1\n")
		
		# Read the current speaker's CSV file	
		csvFile = open(accommodationFileName,'r')								
		csvAlpha = csv.reader(csvFile)

		timeAlpha = []															#  Array of time values
		distanceAlpha = []														#  Array of ratio values

		for record in csvAlpha:
			if record[0].find(taskName) >= 0: 									# If current record is of the current task:
				timeAlpha.append(float(record[1]))								# Add its time value to current task time array
				distanceAlpha.append(0.0 - float(record[2]))					# Add its ratio value to current task ratio array
				if (0.0 - float(record[2])) >= 0.0: 							# If correlation is positive
					counterPositive = counterPositive +1

		spearCoefficient = scipy.stats.spearmanr(timeAlpha,distanceAlpha)[0]
		pValue = scipy.stats.spearmanr(timeAlpha,distanceAlpha)[1]
		length = max(timeAlpha)													# Approximate the end of the task by the start of the last word.
		
	
		# Fuller printout:
		print speakerCode+" "+taskName,",",spearCoefficient,",",abs(spearCoefficient),",",pValue,",",length
		
		
sys.stdout = old_sysout															# Return output stream to console.
outFile.close()

print
print "Correlations complete. Total number of positive correlations: ",counterPositive

print "Modelling and analysis of the " + numStates + " state HMM with " + vectorType + " features complete."
