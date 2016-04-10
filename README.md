# Modelling speakers with HTK
___


[HTK](http://htk.eng.cam.ac.uk/) is a venerable, powerful open software suite for modelling phonemes, words and speakers with Hidden Markov models. It is also a 90s DOS monstrosity which often requires 6 absolute filepaths as parameters and can't safely parse extra whitespace or 
newlines. So you'll want to wrap them in Python scripts... 

...except then you'll still need to read a good chunk of the abstruse 250-page [HTKBook](http://htk.eng.cam.ac.uk/docs/docs.shtml) in order to work out which of the many customisable and redundant modules to call, with which strict .txt file formatting.

So. Here are a set of scripts which take you from a set of tagged .wav speech files all the way to the p-value inference of particular linguistic effects. My aim was detecting 'accommodation' (speech convergence) between pairs of speakers, but the first nine scripts apply to any speaker modelling. 

For anyone interested in the statistical framework, or my results, the resulting paper is [here](https://onedrive.live.com/view.aspx?resid=3D78E8499A8CB205!4594&ithint=file%2cpdf&app=WordPdf&authkey=!AEkaXQxdCVxEG1s).

___

It's an amazing fact that weapons-grade speech recognition and machine learning tools are free and efficient enough for absolutely anyone to (theoretically) apply. 
But it took me 6 weeks to grok the maths, and the software, and write the Python which makes the process painless. My eventual aim is to write a general Python wrapper 
which will allow anyone to model static and dynamic features of their and their friends' linguistics without understanding
the formalism or HTK's txt file peculiarities.

___

1. getAudioSegments.py - break up conversation files into words, given annotations.
2. getScpFile.py - create a 'script file' (list of source wavs and target vector files).
3. getLabels.py - create placeholders with the speaker name and the time of utterance
4. getFeatureVectors.py - creates vectors from .wav files
5. getLabelsFromVectors.py - derives labels from the vector files
6. hmmInitialization.py - one model per speaker, sets means and variances.
7. hmmAddingGaussians.py - multiplying the number of Gaussians for each model.
8. hmmTraining.py - training the models by embedded re-estimation
8b. getLattice - parse the task grammar and verify the model syntax.
9. hmmTesting.py - finds two model likelihoods for each word; one for the word's speaker and one for their interlocutor.
10. getAccommodation.py - calculates all log likelihood ratios for words from paired speakers.
11. getCorrelations.py - calculates the correlation of the ratios.
0. Superscript.py - all of the above.
