# takes in a list of string and turns them into a list of features
from __future__ import division
import nltk
from collections import Counter
from extractors.pos_syntactic import build_tree
import math


"""
=============================================================

HELPER FUNCTIONS

=============================================================
"""


# input: NLP object for one paragraph
# returns: Returns length of phrases in utterance w.r.t. number of words
def getPhraseLength(nlp_obj, phrase_type):

    def count(node, multiplier):

        if node.key == phrase_type:
            multiplier += 1

        # its a word!
        if node.phrase:

            return multiplier * len(node.phrase.split(' '))

        phrase_length = 0

        for child in node.children:
            phrase_length += count(child, multiplier)

        return phrase_length

    # build the syntactic tree

    Phrase_length = 0

    for tree in nlp_obj['parse_tree']:

        root = build_tree(tree)
        multiplier = 0

        if root.key == phrase_type:
            multiplier += 1

        for child in root.children:
            Phrase_length = count(child, multiplier)

    return Phrase_length


# input: NLP object for one paragraph
# returns: Returns count of phrases in utterance with embedded phrases of the
# same type included in the calculation
def getPhraseCountEmbedded(nlp_obj, phrase_type):

    def count(node):

        phrase_count = 0

        if node.key == phrase_type:
            phrase_count += 1

        # its a word!
        if node.phrase:
            return phrase_count

        for child in node.children:
            phrase_count += count(child)

        return phrase_count

    Phrase_count = 0
    for tree in nlp_obj['parse_tree']:
        # build the syntactic tree
        root = build_tree(tree)

        if root.key == phrase_type:
            Phrase_count += 1

        for child in root.children:
            Phrase_count += count(child)

    return Phrase_count


# input: NLP object for one paragraph
# returns: Returns count of phrases in utterance so only the largest phrase parent counts
# but not its children
def getPhraseCountNonEmbedded(nlp_obj, phrase_type):

    def count(node):

        # We've hit our phrase type and can backtrac
        if node.key == phrase_type:
            return 1

        else:

            # its a word!
            if node.phrase:
                return 0

            phrase_count = 0

            for child in node.children:
                phrase_count += count(child)

            return phrase_count

    Phrase_count = 0
    # build the syntactic tree
    for tree in nlp_obj['parse_tree']:

        root = build_tree(tree)

        if root.key == phrase_type:
            Phrase_count += 1

        for child in root.children:
            Phrase_count += count(child)

    return Phrase_count


"""
=============================================================

WORD TYPE COUNTS

=============================================================
"""

# Tag lists
NOUNS = ['NN', 'NNP', 'NNS', 'NNPS']
VERBS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
INFLECTED_VERBS = ['VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
DETERMINERS = ['DT', 'PDT', 'WDT']
ADVERBS = ['RB', 'RBR', 'RBS', 'WRB']
ADJECTIVES = ['JJ', 'JJR', 'JJS']
INTERJECTIONS = ['UH']
SUB_CONJUNCTIONS = ['IN']
COORD_CONJUNCTIONS = ['CC']


# input:
#   nlp_obj: NLP object for one paragraph
#   tag_list: pos tags that form the desired word type
# returns: number of normalized nouns in text
def getNumWordType(nlp_obj, tag_list):

    pos_freq = nlp_obj['pos_freq']

    if pos_freq['SUM'] == 0:
        return 0

    wt_count = 0
    for tag in tag_list:
        wt_count += pos_freq[tag]

    return wt_count / pos_freq['SUM']


"""
===========================================================

WORD TYPE RATIOS

===========================================================
"""


# input: NLP object for one paragraph
# returns: ratio of nouns to verbs in the paragraph
def getRatioVerb(nlp_obj):

    pos_freq = nlp_obj['pos_freq']
    num_nouns = pos_freq['NN'] + pos_freq['NNP'] + pos_freq['NNS'] + pos_freq['NNPS']
    num_verbs = pos_freq['VB'] + pos_freq['VBD'] + pos_freq['VBG'] + pos_freq['VBN'] + pos_freq['VBP'] + pos_freq['VBZ']

    return num_nouns / (num_verbs + 1)


# input: NLP object for one paragraph
# returns: ratio of nouns to verbs in the paragraph
def getRatioNoun(nlp_obj):

    pos_freq = nlp_obj['pos_freq']
    num_nouns = pos_freq['NN'] + pos_freq['NNP'] + pos_freq['NNS'] + pos_freq['NNPS']
    num_verbs = pos_freq['VB'] + pos_freq['VBD'] + pos_freq['VBG'] + pos_freq['VBN'] + pos_freq['VBP'] + pos_freq['VBZ']

    return num_nouns / (num_nouns + num_verbs + 1)


# input: NLP object for one paragraph
# returns: ratio of pronouns to nouns in the paragraph
def getRatioPronoun(nlp_obj):

    pos_freq = nlp_obj['pos_freq']
    num_nouns = pos_freq['NN'] + pos_freq['NNP'] + pos_freq['NNS'] + pos_freq['NNPS']
    num_pronouns = pos_freq['PRP'] + pos_freq['PRP$'] + pos_freq['PRP'] + pos_freq['WHP'] + pos_freq['WP$']

    return num_pronouns / (num_nouns + 1)


# input: NLP object for one paragraph
# returns: ratio of coordinate to subordinate conjunctions in the paragraph
def getRatioCoordinate(nlp_obj):

    pos_freq = nlp_obj['pos_freq']

    return pos_freq['CC'] / (pos_freq['IN'] + 1)


# input: NLP object for one paragraph
# returns: ratio of  types to tokens
def getTTR(nlp_obj):

    num_types = len(set(nlp_obj['token']))
    num_words = len(nlp_obj['token'])

    return num_types / num_words


# input: NLP object for one paragraph
# returns: average ratio of types to tokens using a sliding window
def getMATTR(nlp_obj):

    window = 20
    total_len = len(nlp_obj['token'])

    words_table = Counter(nlp_obj['token'][0:window])
    uniq = len(set(words_table))

    moving_ttr = list([uniq / window])

    for i in range(window, total_len):

        word_to_remove = nlp_obj['token'][i - window]
        words_table[word_to_remove] -= 1

        if words_table[word_to_remove] == 0:

            uniq -= 1

        next_word = nlp_obj['token'][i]
        words_table[next_word] += 1

        if words_table[next_word] == 1:

            uniq += 1

        moving_ttr.append(uniq / window)

    return sum(moving_ttr) / len(moving_ttr)


# input: NLP object for one paragrah
# returns: Brunet index for that paragraph
def getBrunetIndex(nlp_obj):

    # number of word types
    word_types = len(set(nlp_obj['token']))

    # number of words
    words = len(nlp_obj['token'])

    # Brunet's index
    return words**(word_types * -0.165)

# input: NLP object for one paragrah
# returns: Honore statistic for that paragraph


def getHonoreStatistic(nlp_obj):

    # number of word types
    word_types = len(set(nlp_obj['token']))

    # number of words
    words = len(nlp_obj['token'])

    words_table = Counter(nlp_obj['token'])

    words_occuring_once = len([word for word in nlp_obj['token'] if words_table[word] == 1])

    # unlikely case
    if word_types == 0:
        return 0

    if words_occuring_once / word_types == 1:
        return (100 * math.log(words)) / (2 - words_occuring_once / word_types)

    return (100 * math.log(words)) / (1 - words_occuring_once / (word_types))


# input: NLP object for one paragrah
# returns: Mean word length
def getMeanWordLength(nlp_obj):

    tokens = nlp_obj['token']

    word_length = [len(word) for word in tokens]

    # Just to prevent crash
    if len(tokens) == 0:
        return 0

    return sum(word_length) / len(tokens)

# input: NLP object for one paragrah
# returns: number of NID words (length > 2) in paragraph


def getNumberOfNID(nlp_obj):

    pos_tag = nlp_obj['pos']

    foreign_words = [word_pos for word_pos in pos_tag if len(word_pos[0]) > 2 and word_pos[1] == 'FW']

    return len(foreign_words)

# input: NLP object for one paragraph
# returns: normalized number of "uh" and "um"


def getDisfluencyFrequency(nlp_obj):

    tokens = nlp_obj['token']

    um_uh_words = [word for word in tokens if word == 'um' or word == 'uh']

    # just to prevent crash
    if len(tokens) == 0:
        return 0

    return len(um_uh_words) / len(tokens)


# input: NLP object for one paragraph
# returns: Get total number of words excluding NID and filled pauses
def getTotalNumberOfWords(nlp_obj):

    tokens = nlp_obj['token']
    pos_tag = nlp_obj['pos']

    foreign_words = [word_pos for word_pos in pos_tag if word_pos[1] == 'FW']
    um_uh_words = [word for word in tokens if word == 'um' or word == 'uh']

    return len(tokens) - len(foreign_words) - len(um_uh_words)

# input: NLP object for one paragraph
# returns: Returns mean length of sentence w.r.t. number of words


def getMeanLengthOfSentence(nlp_obj):

    raw_text = nlp_obj['raw']
    tokens = nlp_obj['token']
    n_sentences = len(nltk.tokenize.sent_tokenize(raw_text))
    n_words = len(tokens)

    # just to prevent crash
    if n_words == 0:
        return 0

    return n_sentences / n_words

"""

======================================================

 PHRASE TYPE FEATURES

======================================================

"""

# input: NLP object for one paragraph
# returns: Returns proportion of "tkn_type" phrases in utterance w.r.t. number of words
def getProportion(nlp_obj, tkn_type):
    word_count = len(nlp_obj['token'])

    # Prevent crash
    if word_count == 0:
        return 0

    return getPhraseLength(nlp_obj, tkn_type) / word_count

# input: NLP object for one paragraph
# returns: Returns average length (in words) of "tkn_type" phrases in utterance w.r.t. number of "tkn_type" phrases
# This is embedded so subphrases are also counted
def getAvgLengthEmbedded(nlp_obj, tkn_type):

    # phrase length in words summed up
    phrase_length = getPhraseLength(nlp_obj, tkn_type)

    phrase_count = getPhraseCountEmbedded(nlp_obj, tkn_type)

    # Prevent crash
    if phrase_count == 0:
        return 0

    return phrase_length / phrase_count

# input: NLP object for one paragraph
# returns: Returns average length (in words) of "tkn_type" phrases in utterance w.r.t. number of "tkn_type" phrases
# This is non-embedded so only the largest phrase type is counted
def getAvgLengthNonEmbedded(nlp_obj, tkn_type):

    # phrase length in words summed up
    phrase_length = getPhraseLength(nlp_obj, tkn_type)

    phrase_count = getPhraseCountNonEmbedded(nlp_obj, tkn_type)

    # Prevent crash
    if phrase_count == 0:
        return 0

    return phrase_length / phrase_count

# input: NLP object for one paragraph
# returns: Returns number of "tkn_type" phrases divided by the number of words in the sentence
# ATTENTION we use the nonembbeded count here
def getTypeRate(nlp_obj, tkn_type):

    word_count = len(nlp_obj['token'])
    phrase_count = getPhraseCountNonEmbedded(nlp_obj, tkn_type)

    # Prevent crash
    if word_count == 0:
        return 0

    return phrase_count / word_count


# input: list of utterances for one interview stored as [{},{},{}]
# returns: list of features for  interview
def get_all(interview):
    features = {}
    # POS counts
    features["NumNouns"] = sum([getNumWordType(utterance, NOUNS) for utterance in interview]) / len(interview)
    features["NumVerbs"] = sum([getNumWordType(utterance, VERBS) for utterance in interview]) / len(interview)
    features["MATTR"] = sum([getMATTR(utterance) for utterance in interview]) / len(interview)
    features["BrunetIndex"] = sum([getBrunetIndex(utterance) for utterance in interview]) / len(interview)
    features["HonoreStatistic"] = sum([getHonoreStatistic(utterance) for utterance in interview]) / len(interview)

    # Summary statistics
    features["NumberOfNID"] = sum([getNumberOfNID(utterance) for utterance in interview]) / len(interview)
    features["MeanWordLength"] = sum([getMeanWordLength(utterance) for utterance in interview]) / len(interview)
    features["TotalNumberOfWords"] = sum([getTotalNumberOfWords(utterance) for utterance in interview]) / len(interview)
    features["DisfluencyFrequency"] = sum([getDisfluencyFrequency(utterance) for utterance in interview]) / len(interview)

    # Phrase features/len(interview)
    features["NumAdverbs"] = sum([getNumWordType(utterance, ADVERBS) for utterance in interview]) / len(interview)
    features["NumAdjectives"] = sum([getNumWordType(utterance, ADJECTIVES) for utterance in interview]) / len(interview)
    features["NumDeterminers"] = sum([getNumWordType(utterance, DETERMINERS) for utterance in interview]) / len(interview)
    features["NumInterjections"] = sum([getNumWordType(utterance, INTERJECTIONS) for utterance in interview]) / len(interview)
    features["NumInflectedVerbs"] = sum([getNumWordType(utterance, INFLECTED_VERBS) for utterance in interview]) / len(interview)
    features["NumCoordinateConjunctions"] = sum([getNumWordType(utterance, COORD_CONJUNCTIONS) for utterance in interview]) / len(interview)
    features["NumSubordinateConjunctions"] = sum([getNumWordType(utterance, SUB_CONJUNCTIONS) for utterance in interview]) / len(interview)

    # POS ratios
    features["RatioNoun"] = sum([getRatioNoun(utterance) for utterance in interview]) / len(interview)
    features["RatioVerb"] = sum([getRatioVerb(utterance) for utterance in interview]) / len(interview)
    features["RatioPronoun"] = sum([getRatioPronoun(utterance) for utterance in interview]) / len(interview)
    features["RatioCoordinate"] = sum([getRatioCoordinate(utterance) for utterance in interview]) / len(interview)

    # Weird statistics
    features["TTR"] = sum([getTTR(utterance) for utterance in interview]) / len(interview)
    features["NPTypeRate"] = sum([getTypeRate(utterance, 'NP') for utterance in interview]) / len(interview)
    features["VPTypeRate"] = sum([getTypeRate(utterance, 'VP') for utterance in interview]) / len(interview)
    features["PPTypeRate"] = sum([getTypeRate(utterance, 'PP') for utterance in interview]) / len(interview)
    features["NPProportion"] = sum([getProportion(utterance, 'NP') for utterance in interview]) / len(interview)
    features["VPProportion"] = sum([getProportion(utterance, 'VP') for utterance in interview]) / len(interview)
    features["PProportion"] = sum([getProportion(utterance, 'PP') for utterance in interview]) / len(interview)
    features["AvgNPTypeLengthEmbedded"] = sum([getAvgLengthEmbedded(utterance, 'NP') for utterance in interview]) / len(interview)
    features["AvgVPTypeLengthEmbedded"] = sum([getAvgLengthEmbedded(utterance, 'VP') for utterance in interview]) / len(interview)
    features["AvgPPTypeLengthEmbedded"] = sum([getAvgLengthEmbedded(utterance, 'PP') for utterance in interview]) / len(interview)
    features["AvgNPTypeLengthNonEmbedded"] = sum([getAvgLengthNonEmbedded(utterance, 'NP') for utterance in interview]) / len(interview)
    features["AvgVPTypeLengthNonEmbedded"] = sum([getAvgLengthNonEmbedded(utterance, 'VP') for utterance in interview]) / len(interview)
    features["AvgPPTypeLengthNonEmbedded"] = sum([getAvgLengthNonEmbedded(utterance, 'PP') for utterance in interview]) / len(interview)

    return features
