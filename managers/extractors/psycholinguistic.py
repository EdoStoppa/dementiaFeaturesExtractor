from nltk.corpus import stopwords
import pandas as pd
import os


# Made global so files only need to be read once
psycholinguistic_scores = {}
subtlex_data = None

# -------------------------------------

# Constants
FEATURE_DATA_LIST = ["familiarity", "concreteness", "imageability", 'aoa']

# ================================================
# -------------------Tools------------------------
# ================================================
def getAllWordsFromInterview(interview):
    words = []
    for uttr in interview:
        words += [word.lower() for word in uttr["token"] if word.isalpha()]
    return words


def getAllNonStopWordsFromInterview(interview):
    stop = stopwords.words('english')
    words = []
    for uttr in interview:
        words += [word.lower() for word in uttr["token"] if word.isalpha() and word not in stop]
    return words

# ================================================
# -----------Psycholinguistic features------------
# ================================================

# Input: one of "familiarity", "concreteness", "imageability", or 'aoa'
# Output: none
# Notes: Makes dict mapping words to score, store dict in psycholinguistic
def _load_scores(feature_data_path, name):
    if name not in FEATURE_DATA_LIST:
        raise ValueError("name must be one of: " + str(FEATURE_DATA_LIST))
    with open(os.path.join(feature_data_path, name)) as file:
        d = {word.lower(): float(score) for (score, word) in [line.strip().split(" ") for line in file]}
        psycholinguistic_scores[name] = d

# Input: Interview is a list of utterance dictionaries, measure is one of "familiarity", "concreteness", "imageability", or 'aoa'
# Output: PsycholinguisticScore for a given measure


def getPsycholinguisticScore(interview, path_to_measures, measure):
    if measure not in FEATURE_DATA_LIST:
        raise ValueError("name must be one of: " + str(FEATURE_DATA_LIST))
    if measure not in psycholinguistic_scores:
        _load_scores(path_to_measures, measure)
    score = 0
    validwords = 1
    allwords = getAllNonStopWordsFromInterview(interview)
    for w in allwords:
        if w.lower() in psycholinguistic_scores[measure]:
            score += psycholinguistic_scores[measure][w.lower()]
            validwords += 1
    # Only normalize by words present in dict
    return score / validwords


def getSUBTLWordScores(interview, subl_path):
    allwords = getAllNonStopWordsFromInterview(interview)

    # If first call, load all frequency data from memory
    global subtlex_data
    if subtlex_data is None:
        subtlex_data = pd.read_csv(subl_path)
        subtlex_data = pd.Series(subtlex_data.SUBTLWF.values,index=subtlex_data.Word).to_dict()

    # Get the frequency of all found words
    freq = []
    for word in allwords:
        if word in subtlex_data:
            freq.append(float(subtlex_data[word]))

    return 0 if len(allwords) == 0 else sum(freq) / len(allwords)

# input: list of interview utterances stored as [ [{},{},{}], [{},{},{}] ]
# returns: list of features for each interview
def get_psycholinguistic_features(interview, subtl_path, path_to_measures):
    feat_dict = {}
    feat_dict["getFamiliarityScore"] = getPsycholinguisticScore(interview, path_to_measures, 'familiarity')
    feat_dict["getConcretenessScore"] = getPsycholinguisticScore(interview, path_to_measures, 'concreteness')
    feat_dict["getImageabilityScore"] = getPsycholinguisticScore(interview, path_to_measures, 'imageability')
    feat_dict["getAoaScore"] = getPsycholinguisticScore(interview, path_to_measures, 'aoa')
    feat_dict["getSUBTLWordScores"] = getSUBTLWordScores(interview, subtl_path)

    return feat_dict

if __name__ == '__main__':
    pass



