# *Dementia Features Extractor*
The objective of this project is to create a modular and extensible framework that is able to extract different groups of features from the transcripts and audio files of the DementiaBank dataset. In particular, the data used will be only the part associated with the Cookie Theft Picture test. To download the database, you'll have to get access directly on the [DementiaBank website](https://dementia.talkbank.org/). This work is published in the proceeding of the 2022 IEEE 7th Forum on Research and Technologies for Society and Industry Innovation: Stoppa, E. and Di Donato, G and Parde, N. and Santambrogio, M. "Computer-Aided Dementia Detection: How Informative are Your Features?" IEEE RTSI 2022.

---

## Credits
Most of the code that compute the numerical features is based on [this project](https://github.com/vmasrani/dementia_classifier/tree/master/dementia_classifier/feature_extraction/feature_sets), but it was greatly modified to increase efficiency, to fix some errors, and to reduce code redundancy. For the preprocessing I've taken some parts from [this project](https://github.com/flaviodipalo/AlzheimerDetection), again updating it and fixing some minor errors. 

---

## Prerequisites
I recommend to use Python 3+ and Linux/MacOs to avoid any problems. Unfortunately, to extract some features it's required an old library (from 2016), and some parts of it, for some reason, refuse to work on Windows. It probably can be fixed, but I've no idea how.

### - External Libraries
First, download the libraries from [here](https://drive.google.com/file/d/1JVH9QIOcrK3ewzSzIPnr6q7Gug_Roex9/view?usp=sharing). Then, extract it and place the `lib` folder into `managers/extractors/`. Now every extrenal library outside of Python should be ready to be used.
To run the preprocessing the Stanford CoreNLP library is required. It must be run in a separate terminal before the start of preprocessing. The command to run it from the main project folder is:

```
java -DIM -cp "extractors/feature_sets/lib/stanford/stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 20000
```

Where instead of `-DIM` you'll have to substitute `-Xmx500m` if using Windows, or `-Xmx4g` if using Linux/MacOS.

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
Download all transcripts and audio files of the Pitt's Corpus from DementiaBank (for the audio files I reccomend using the Multi-file Downloader extension for Chrome or Firefox). The anagraphic data is available without any special access right, so I've included the csv file directly in the repository. 

Insert all files in the `data` folder following this folders structure:

```
data
│
├── anagraphic_data/
│
├── audiomp3/
│   ├── Control/
│   │   └── cookie/
│   └── Dementia/
│       └── cookie/
│
├── discours_trees/
│   ├── control/
│   │   ├── doc/
│   │   ├── seg/
│   │   └── sent/
│   └── dementia/
│       ├── doc/
│       ├── seg/
│       └── sent/
│
├── extracted/
│
├── SUBTLEX/
│
└── transcripts/
    ├── Control/
    │   └── cookie/
    └── Dementia/
        └── cookie/
```
For now everything that should be inside the folder `data/discourse_trees` will be provided directly from me. Just write me an email at estopp2@uic.edu and I'll send the data required. In the future I'll try to recreate the scripts necessary to generate this missing data and I'll include those in this repository.

---

## How to run
Please pay attention to the mp3 to wav audio file conversion. It takes a lot of memory. To reduce the wasted space, you can set to True the paramenter called "remove_mp3" in the function `mp3_to_wav.convert()` in `run.py`. Doing so will delete the (now useless) old mp3 file immediately after the conversion.

### - All in one
After following the prerequisites section, to extract all the features simply run the file `run.py` from the main folder using `python run.py`. The results will be in `data/extracted/`. To be sure that everything goes well, I recommend to run the command with as sudo: `sudo python run.py`.

### - Individual Feature Group
Before running most of the individual scripts, you'll necessarily need to run (always starting from the main folder)<br />
`python managers/preprocess.py`. If you're interest in the audio features you'll also have to run `python mp3_to_wav.py`.

Then, to run any Feature Group, simply run `python extractors/FILE.py`, where "FILE" is the name of the desired file.

---

## How to contribute with new Features
To add a new feature to an already existing group, first create a function that compute the feature and place it in the related extractor. Then add in the `get_all()` function a call to the function that compute the feature and add it to the dictionary that contains all the extracted data. It's as simple as that.

---

## How to contribute with new Feature Groups
To contribute to this framework with new feature groups, you will need to create 2 different Python files: a group `manager` and a group `extractor`.

### - Group Manager
This will be mainly in charge of loading any data needed for the extraction, collecting any dictionary containing the extracted features, and saving everything in a csv file. There's no strict rule on how a manager should operate, but the two main types of workflow can be observed in `acoustic_mng.py` and `psycholinguistic_mng.py`, so give them a look before creating a new manager. In the end every manager should have a method called `extract_{FEATURE GROUP NAME}` that execute the feature extraction.

### - Group Extractor
This is a file (or some files) where all the code needed to the actual extraction of the numerical features is collected. This means that the code will be full of supporting functions or functions that compute a specific feature. For each feature extractor there must be a function called `get_all()` that will use all the other specified functions to collect the features. It will return a dictionary containing the features for a conversation, or a list of dictionaries containing the features
of the conversations. To better understand how it works, please take a look at `acoustic.py` and at `spatial.py`. For now all extractors and eventual support files will be store in the same folder, but if the file number increases too much we will reorganize the extractor folder using a subfolder for each feature group.
