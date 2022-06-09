# encoding: utf-8
import os
import sys
import re
import requests
import nltk
from collections import defaultdict
import feature_sets.util as util
import nltk.data
import pickle

# Use the name of the extracted folder
STANFORD_DIR = 'stanford-corenlp-full-2015-12-09'
# With Linux/MacOS us '-Xmx4g', with Windows use '-Xmx500m'
MEMORY_DIM = '-Xmx4g'

def get_stanford_parse(sentence, port=9000):
    re.sub(r'[^\x00-\x7f]', r'', sentence)
    sentence = util.remove_control_chars(sentence)
    try:
        r = requests.post('http://localhost:' + str(port) +
                          '/?properties={\"annotators\":\"parse\",\"outputFormat\":\"json\"}', data=sentence)
    except requests.exceptions.ConnectionError as e:
        print ("We received the following error in get_data.get_stanford_parse():")
        print (e)
        print ("------------------")
        print ('Did you start the Stanford server? If not, try:\n java ' + MEMORY_DIM + 
               ' -cp "lib/stanford/' + STANFORD_DIR + '/*" ' + 
               'edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 20000')
        print ("------------------")
        sys.exit(1)

    json_obj = r.json()
    return json_obj['sentences'][0]


def preprocess_utterance(uttr):
    uttr = util.clean_uttr(uttr)         # clean
    tokens = nltk.word_tokenize(uttr)    # Tokenize
    tagged_words = nltk.pos_tag(tokens)  # Tag

    # Get the frequency of every type
    pos_freq = defaultdict(int)
    for word, wordtype in tagged_words:
        pos_freq[wordtype] += 1

    pos_freq['SUM'] = len(tokens)
    pt_list = []
    bd_list = []
    for u in util.split_string_by_words(uttr, 50): # 50 = max number of words in a utterance
        if u is not "":
            stan_parse = get_stanford_parse(u)
            pt_list.append(stan_parse["parse"])
            bd_list.append(stan_parse["basic-dependencies"])
    datum = {"pos": tagged_words, "raw": uttr, "token": tokens,
             "pos_freq": pos_freq, "parse_tree": pt_list, "basic_dependencies": bd_list}
    return datum


# Extract data from dbank directory
def parse_file_dementiabank(file):
    session_utterances = []
    for line in file:
        uttr = util.clean_uttr(line)
        if util.isValid(uttr):
            session_utterances.append(preprocess_utterance(uttr))

    return session_utterances

def clean_file(input_file):
    '''
    :param input_file: single dataset file as readed by Python
    :return: tokenized string of a single patient interview
    '''
    cleaned_file = []
    id_string = input_file.name.split(os.path.sep)[-1]
    result = re.search('(.*).cha', id_string)
    id = result.group(1)
    for line in input_file:
        for element in line.split("\n"):
            if "*PAR" in element:
                # substitute any '?' or '!' with '.'
                cleaned_string = re.sub(r'(\?|\!)', '.', element) #element.replace('?', '.')
                # remove pause pattern.
                cleaned_string =  re.sub(r'\([\d]*(\.)+[\d]*\)\s', '', cleaned_string)
                #remove any word after the period.
                cleaned_string = cleaned_string.split('.', 1)[0]
                #replace par with empty string, deleting the part of the string that starts with PAR
                cleaned_string = re.sub(r'[^\w]+', ' ', cleaned_string.replace('*PAR',''))
                #substitute numerical digits, deleting underscores
                cleaned_string = re.sub(r'[\d]+','',cleaned_string.replace('_',''))
                cleaned_file.append(cleaned_string)
    return cleaned_file, id

def generate_full_interview_dataframe(prj_dir: str):
    """
    generates the pandas dataframe containing for each interview its label.
    :return: pandas dataframe.
    """
    dementia_parsed = {}
    for label in ["Control", "Dementia"]:
        for test in ['cookie']:
            PATH = os.path.join(prj_dir, 'data', 'transcripts', label, test)
            for path, dirs, files in os.walk(PATH):
                for filename in files:
                    fullpath = os.path.join(path, filename)
                    with open(fullpath, 'r', encoding="utf8") as input_file:
                        print('Preprocessing ' + filename + '...')
                        cleaned_file, id = clean_file(input_file)
                        parsed_file = parse_file_dementiabank(cleaned_file)
                        dementia_parsed[id] = (parsed_file, label)
    
    return dementia_parsed

def preprocess_data(prj_dir: str):
    print('\nPreprocessing started!\n')
    # Generate the data
    data = generate_full_interview_dataframe(prj_dir)
    # Save all processed data
    final_path = os.path.join(prj_dir, 'data', 'pitt_full_interview.pickle')
    with open(final_path, 'wb') as f:
        pickle.dump(data, f)
    print('\nPreprocessing finished!\n')
    print('*****************************************************')

if __name__ =='__main__':
    preprocess_data()