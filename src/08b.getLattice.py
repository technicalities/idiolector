import sys
import os

# This script builds a word-recognition network from the Backus-Naur grammar.
# In our case, it is a very simple lattice, involving one 'word' (the speaker model).

# The input arguments are:
# 	1) a speaker's code
#	2) the corresponding simple BN grammar file path.

#  The outputs are "Syntax" files in the format [speakercode]Syntax.txt.
							

# Definition of paths
rootDirectory = "F:/Accommodation/Files/"
syntaxPath = rootDirectory+ "Lists/Syntax/"													
grammarPath = rootDirectory+ "Lists/Grammars/"												


# Config variables.
varianceFloor = "0.000001"
verbosityLevel = "00004"

speakerArray = ["ARA14", "GJN14", "HLH30", "JSE11",
				"JTN20", "JYN22", "KBN30", "SCA01", 
				"SHA13", "SKN03", "TMY30", "ZSE07"]		
				

for index in range(len(speakerArray)):

	speakerCode = speakerArray[index]														#  The speaker model to test.							
	modelsListName = rootDirectory + "Lists/SpeakerPairs/" + speakerCode + ".txt"			#  File containing chosen speaker and their paired speaker.
	grammarName = grammarPath + speakerCode + "Grammar.txt"
	syntaxName = syntaxPath + speakerCode + "Syntax.txt" 									#  Generated schema of speaker
	dictionaryName = dictionaryPath + speakerCode + "Dictionary.txt"
	
# Parses the Backus-Naur grammar ('grammar') into a word network ('syntax')
	print "HParse",">>>>>"
	command = "HParse"
	command = command+" "+ grammarName
	command = command+" "+ syntaxName
	command = command+" -T "+ verbosityLevel
	
	os.system(command)
