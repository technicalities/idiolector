import sys
import os
import csv
import wave

# This script gets audio segments from the conversation data by using the LaBB-CAT files.

#  The input parameters are:
# 		1) Labb-cat data as csv file.
# 		2) Name of original .wav conversation file
# 	The outputs are:
# 		1) an individual .wav audio file for every word.


#  List of codes representing the twelve Diapix tasks.
taskArray = ["raB_1_", "raB_2_", "raB_3_", "raB_4_",
			"raF_1_", "raF_2_", "raF_3_", "raF_4_",
			"raS_1_", "raS_2_", "raS_3_", "raS_4_"]

# Initialization
rootDirectory = "F:/Accommodation/Files/"
labbCatPath = rootDirectory + "1.LaBB-CAT/"
audioFilePath = rootDirectory + "wavReal/"								# NB: Folder is large, 2GB. Included separately, as Dropbox folder.
wavWordsPath = rootDirectory + "2.WavWords/"
speakerCode = sys.argv[1]



for index in range(len(taskArray)):

	labbcatFileName = labbCatPath + taskArray[index] + speakerCode+ ".csv"
	audioFileName = audioFilePath + taskArray[index] + speakerCode+ ".wav"
	
	# Acquisition of the labbcat file
	labbcatFile = open(labbcatFileName,'r')
	labbcatData = csv.reader(labbcatFile)

	# Opening wav file
	origAudio = wave.open(audioFileName,'r')
	frameRate = origAudio.getframerate()
	nChannels = origAudio.getnchannels()
	sampWidth = origAudio.getsampwidth()

	# Loop over the records of the labb-cat-file (csv format)
	labbcatData.next()

	for record in labbcatData:	
		if record[12] != "" and record[13] != "" and record[3] == speakerCode:	
			record[11] = record[11].replace("'","")
			record[11] = record[11].replace("\\","",3)
				
			start = float(float(record[12]))
			end = float(float(record[13]))
			
			origAudio.setpos(int(start*frameRate))
			chunkData = origAudio.readframes(int((end-start)*frameRate))
			
			# Limiting the number of decimal digits in the start time. 
			if '.' in record[12]:
				if len(record[12]) >= record[12].index('.')+4:
					record[12] = record[12][0:record[12].index('.')+4]
			else:	
				record[12] = record[12]+".000"
				
			outFileName = wavWordsPath+record[2].split('.')[0]+'-'+record[11]+'-'+record[12]+".wav"
			print outFileName,int((end-start)*frameRate),int(start*frameRate)
		
			chunkAudio = wave.open(outFileName,'w')
			chunkAudio.setnchannels(nChannels)
			chunkAudio.setsampwidth(sampWidth)
			chunkAudio.setframerate(frameRate)
			chunkAudio.writeframes(chunkData)
			chunkAudio.close()
