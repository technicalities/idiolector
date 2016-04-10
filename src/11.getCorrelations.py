import csv
import sys
import scipy.stats

#  This program plots the accommodation data and derives a correlation from the point likelihood ratios over time.

#  Inputs are one .csv file per speaker, listing the log-likelihood ratio for each of their words.
#  Output is one csv file summarising the correlation between log-likelihood and time, for each analysis unit (speaker i on task j).


# Initialisation.
numStates = raw_input("Enter number of states in model as a word (e.g. 'One', 'Two'): ")			
vectorType = raw_input("Enter type of vector used (e.g. 'MFCC' or 'LPC'): ")

speakerArray = ["ARA14", "GJN14", "HLH30", "JSE11",
			"JTN20", "JYN22", "KBN30", "SCA01",
			"SHA13", "SKN03", "TMY30", "ZSE07"]

counterPositive = 0																# Counter for the total no. of positive correlations.
			
			
# Path names.
modelPath = numStates + "State/" + vectorType
rootDirectory = "F:/Accommodation/Files/"
taskPath = rootDirectory + "Lists/TestDataLists/TestTasks/"
accommPath = rootDirectory + "7.Outputs/Accommodations/" + modelPath + "/"
outputFile = rootDirectory + "7.Outputs/Correlations/" + modelPath + "rawOutput.csv" 		


# Redirect standard output stream:
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
		csv = csv.reader(csvFile)

		timeArray = []															#  Array of time values
		distanceArray = []														#  Array of ratio values

		for record in csv:
			if record[0].find(taskName) >= 0: 									# If current record is of the current task:
				time.append(float(record[1]))								# Add its time value to current task time array
				distanceArray.append(0.0 - float(record[2]))					# Add its ratio value to current task ratio array
				if (0.0 - float(record[2])) >= 0.0: 							# If correlation is positive
					counterPositive = counterPositive +1

		spearCoefficient = scipy.stats.spearmanr(timeArray,distanceArray)[0]
		pValue = scipy.stats.spearmanr(timeArray,distanceArray)[1]
		length = max(timeAlpha)													# Approximate the end of the task by the start of the last word.
		
	
		# Fuller printout:
		print speakerCode+" "+taskName,",",spearCoefficient,",",abs(spearCoefficient),",",pValue,",",length
		
		
sys.stdout = old_sysout															# Return output stream to console.
outFile.close()
print
print "Correlations complete. Total number of positive correlations: ",counterPositive


