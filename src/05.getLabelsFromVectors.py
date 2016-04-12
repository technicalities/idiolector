import sys
import os
import wave

#  This script creates the label files associated with each vector.
#  (reads a vector file and writes the corresponding label). 
#  The input argument is: 
#	1) the type of vector feature to label.

#  Outputs: One label for each vector file input 
# 			in the format [0] [end time] [word]

# Initialization
vectorType = raw_input("Enter type of vector to create labels for (e.g. 'MFCC' or 'LPC'): ")

# Convert arguments to upper-case if they are not:
if not (vectorType.isupper()):
	vectorType = vectorType.upper()
	

# Definition of paths
vectorFolder = "3.Vectors/"+ vectorType + "/"
labelFolder = "4.Labels/speakerLabels/"
rootDirectory ="F:/Accommodation/Files/"
vectorFilesPath = rootDirectory + vectorFolder					# Directory of source vector files.
labelFilesPath = rootDirectory + "4.Labels/" + labelFolder		# Directory of target label files.
listPath = rootDirectory+ "Lists/VectorLists/"
vectorListFileName = listPath + "All_" + vectorType + "s.txt"	# Path of full list of source vector files.

# To read the vector file list:
vectorListFile = open(vectorListFileName,'r')
vectorList = vectorListFile.readlines()
vectorListFile.close()


# Processing the vector files and writing the label files
count = 0

for vectorItem in vectorList:
    # Opening the vector file
	fileName = vectorItem[0:len(vectorItem)-1]						# Copy the whole path of the vector.
	command = "HList -h "+ fileName + " > out.dat"					# HList is a vector-reader which we use to extract label info.
	os.system(command)
	
	outFile = open("out.dat",'r')
	outData = outFile.readline()
	outData = outFile.readline()
	outData = outFile.readline()
	outData = outFile.readline()
	outDataList = outData.split()
	outFile.close()

	# Creating the label file: split on dots and then rebuild path after.
	itemLabList = vectorItem.split(".")	
	extension = itemLabList[3] 
	extension = extension[0:len(extension)-1]	 
	itemLab = itemLabList[0] + "."+itemLabList[1]+"."+itemLabList[2] +"."+ extension
	
	if (vectorType == "MFCC") :
		itemLab = itemLab.replace(".mfc",".lab")
	if (vectorType == "LPC") :
		itemLab = itemLab.replace(".lpc",".lab")
	
	itemLab = itemLab.replace(vectorFolder,labelFolder,1)
	speakerCode = itemLab.split('_')[2]
	speakerCode = speakerCode.split('-')[0]

	labFile = open(itemLab,'w')
	labFile.writelines(str(0)+" "+str((int(outDataList[2])-1)*100000)+" "+speakerCode) # Label format: Time extracted in ns
	labFile.close()

	count = count + 1
	if (count % 1000 == 0)
		print "Labels written: ", count, "of", len(vectorList)
	
print("Program completed, written",count,"label files in directory",labelFilesPath)
