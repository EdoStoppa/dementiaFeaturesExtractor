# *Dementia Features Extractor*
The objective of this project is to create a modular program that is able to extract different kind of features from transcripts and audio files from DementiaBank. To obtain access to the actual data, you'l have to get access directly on the [DementiaBank website](https://dementia.talkbank.org/).

---

## Prerequisites
To run everything without problems I recommend to use Python 3.8+ and Linux/MacOs. Unfortunately, to extract some features it's required an old library (from 2014), and some parts of it, for some reason, refuse to work on Windows. It probably can be fixed, but I've no idea how.

### - External Libraries
To run the preprocessing the Stanford CoreNLP library is required. It must be run in a separate terminal before the start of preprocessing. The latest version can be downloaded from [here](https://stanfordnlp.github.io/CoreNLP/download.html). After the download, it must be extracted and positioned under the folder `extractors/feature_sets/lib/standford/`, and the name of the folder must be set in `extractors/preprocess.py`. Everything was tested with version 3.6.0 (stanford-corenlp-full-2015-12-09), but it should also work with any following release.

The last thing needed is to download the L2SCA library from [here](http://www.personal.psu.edu/xxl13/downloads/l2sca.html). Then, extract its content, and put every file in the extracted folder inside `extractors/feature_sets/lib/SCA/L2SCA/` apart from the file `analyzeText.py` that I've modified to male it work with Python 3.

### - Python Libraries
```
- pandas
- numpy
- scipy
- python_speech_features
- nltk
- pydub
- itertools
```

### - Data
Download all transcripts and audio files of the Pitt's Corpus from DementiaBank (for the audio files I reccomend using the Multi-file Downloader for Chrome or Firefox). The anagraphic data is available without any special access right, so I've included the csv file directly in the repository. Then insert all files in the `data` folder following this folders structure:
```
-> data
----> anagraphic_data
----> audiomp3
--------> Control
--------> Dementia
----> discourse_trees
----> extracted
----> SUBTLEX
----> transcripts
--------> Control
--------> Dementia
```

---

## How to run

### - All in one
After following the prerequisites section, to extract all the features simply run the file `run.py` from the main folder using `python run.py`. The results will be in `data/extracted/`.

### - Individual Feature Group
Before running most of the individual scripts, it's better to run (always starting from the main folder) `python extractors/preprocess.py` and `python mp3_to_wav.py`.

Then, to run any Feature Group, simply run `python extractors/FILE.py`, where "FILE" is the name of the desired file.

---

## Credits
Most of the code that compute the numerical features is an adapted and updated version of [this project](https://github.com/vmasrani/dementia_classifier/tree/master/dementia_classifier/feature_extraction/feature_sets). For the preprocessing I've taken some parts from [this other project](https://github.com/flaviodipalo/AlzheimerDetection). 
