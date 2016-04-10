import sys
import os

#  This script calculates the logarithm of the ratio p(x_A|B)/p(x_A|A) for each word.
#  The first prob p(x_A|B) is from tbe "Recognitions/target". It is the probability of x_A being produced by model B. 
#  The second probability p(x_A|A) is the probability of x_A being produced by model A (it is in directory Recognitions/self).

#  The input parameters are: 1) a list of 'target' .rec files (a txt file of pathnames),

#  The output is one .csv file per speaker, listing, for each rec file: 
#    1) file path, 2) the time, 3) the log likelihood ratio, 4) the word, 5) word length in chars, 6) frame number extracted at.


# Initialization
numStates = raw_input("Enter number of states in model as a word ('One', 'Two'): ")									
vectorType = raw_input("Enter the type of vector the transcriptions are from (e.g. 'MFCC' or 'LPC'): ")

# Convert args to uppercase if not:
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
recognitionPath = rootDirectory + "Lists/RecognitionLists/" + modelPath


# For each speaker:
for index in range(len(speakerArray)):

	speakerCode = speakerArray[index]
	recListPath = recognitionPath + speakerCode + "recs.txt"
	# The CSV file to write transcriptions to.
	outputFile = rootDirectory + "7.Outputs/Accommodations/" + modelPath + speakerCode + "accomm.csv" 	

	# Reading the list of rec files
	recListFile = open(recListPath,'r')
	targetRecList = recListFile.readlines()
	recListFile.close()

	count = 0

	# Redirect standard output stream:
	old_sysout = sys.stdout												# Store output stream in temp
	outFile = open(outputFile, 'w')										# New file.
	sys.stdout = outFile												# Redirect print commands to outFile.

	# For each recognition file in the 'target' directory:
	for itemTarget in targetRecList:
		# Getting the name of the rec files
		itemTarget = itemTarget[0:len(itemTarget)-1]					# Pathname of current target rec file.
		itemSelf = itemTarget.replace("target", "self",1)				# Create a path to the equivalent 'self' recognition file.
		
		# Extracting the time from the rec file name
		itemNameList = itemTarget.split('-')							# Produces an Array of: [0] path + task_speaker; [1] word spoken; [2] the time
		timeList = itemNameList[len(itemNameList)-1].split('.')			# Array of: [0] secs time, [1] millisecs time, and [2] ".rec"
		time = float(timeList[0]) + float(timeList[1]) * 0.001			# Divide by 1000 to obtain time
		word = itemNameList[1]
		
		# Extracting the target likelihood
		recFile = open(itemTarget,'r')									
		rec = recFile.readline()
		recFile.close()
		targetLikelihood = float(rec.split()[3])						#  Assign the log likelihood
		frameNumber = float(rec.split()[1])*0.00001						#  Find the frame it was spoken at (division by 10,000).
		
		# Extracting the self likelihood
		recFile = open(itemSelf,'r')
		rec = recFile.readline()
		recFile.close()
		selfLikelihood = float(rec.split()[3])
		itemTargetList = itemTarget.split('/')
		
		ratio = selfLikelihood - targetLikelihood						# Subtracting the logs gives us our B/A ratio.
		
		# Output to CSV in format: [Rec file path, log-likelihood ratio, word spoken, length of word, frame extracted at].
		print itemTargetList[len(itemTargetList)-1],",",time,",",ratio,",",word,",",len(word),",",frameNumber
		
		count = count + 1

		
	sys.stdout = old_sysout
	outFile.close()
	print "Completed computing", count, "likelihoods for", speakerCode

