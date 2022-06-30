# *Dementia Features Extractor*
The objective of this project is to create a modular program that is able to extract different kind of features from transcripts and audio files from DementiaBank. In particular the data used will be only the part associated with the Cookie Theft Picture test. To download the database, you'll have to get access directly on the [DementiaBank website](https://dementia.talkbank.org/).

---

## Prerequisites
I recommend to use Python 3+ and Linux/MacOs to avoid any problems. Unfortunately, to extract some features it's required an old library (from 2016), and some parts of it, for some reason, refuse to work on Windows. It probably can be fixed, but I've no idea how.

### - External Libraries
First, download the libraries from [here](https://drive.google.com/file/d/1O_rvaWWaNn3vxDMbxf3GMlabx9sWbiMG/view?usp=sharing). Then, extract it and place the `lib` folder into `extractors/feature_sets/`. Now every extrenal library outside of Python should be ready to be used.<br \>
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
After following the prerequisites section, to extract all the features simply run the file `run.py` from the main folder using `python run.py`. The results will be in `data/extracted/`.

### - Individual Feature Group
Before running most of the individual scripts, you'll necessarily need to run (always starting from the main folder) `python extractors/preprocess.py`. If you're interest in the audio features you'll also have to run `python mp3_to_wav.py`.

Then, to run any Feature Group, simply run `python extractors/FILE.py`, where "FILE" is the name of the desired file.

---

## Credits
Most of the code that compute the numerical features is an adapted and updated version of [this project](https://github.com/vmasrani/dementia_classifier/tree/master/dementia_classifier/feature_extraction/feature_sets). For the preprocessing I've taken some parts from [this other project](https://github.com/flaviodipalo/AlzheimerDetection). 
