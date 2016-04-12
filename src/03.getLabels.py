
import sys
import os
import wave

# This script creates the label files associated to the wav files
# 1) list of wav files (full name)
# 2) name of the speaker

# Initialization

item = sys.argv[1]

# Definition of paths
rootDirectory = "F:/Accommodation/Files/"
configurationFilePath = rootDirectory + "Lists/config/"
mfccFilesPath = rootDirectory+ "3.MFCCs/"
wavFilesPath = rootDirectory + "2.wavWords/"


# Reading the list of wav files
#wavListFile = open(wavListFileName,'r')
#wavList = wavListFile.readlines()
#wavListFile.close()

#python 4b.getOneFeatureVector.py F:\Accommodation\Files\2.wavWords\raB_4_SHA13-bottom-230.533.wav F:\Accommodation\Files\raB_4_SHA13-bottom-230.533.mfc

# Processing the wav files and writing the label files

count = 0

#item = item[0:len(item)-1]
itemLab = item.replace("2.wavWords","4.Labels",1)
itemLab = itemLab.replace(".wav",".lab",1)

speakerName = item.split('_')[2]
speakerName = speakerName.split('-')[0]
print speakerName

print itemLab

origAudio = wave.open(item,'r')
frameRate = origAudio.getframerate()
nFrames = origAudio.getnframes()
origAudio.close()

wavLen = float(nFrames)*10000000/float(frameRate)
print item,">>",int(wavLen)

# Writing the label file

labFile = open(itemLab,'w')
labFile.writelines(str(0)+" "+str(int(wavLen))+" "+speakerName)
labFile.close()

count = count+1

print "Program completed, written",count,"label files in directory",labelFilesPath






