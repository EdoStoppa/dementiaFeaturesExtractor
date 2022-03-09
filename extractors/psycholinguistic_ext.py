from feature_sets.psycholinguistic import get_psycholinguistic_features
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import pickle
import os

def extract_psycholinguistic():
    sid = SentimentIntensityAnalyzer()

    with open(os.path.join('data', 'pitt_full_interview.pickle'), "rb") as file:
        data = pickle.load(file)

    new_dataframe = []
    for key in data.keys():
        print('Processing ' + str(key) + '...')
        full_interview, label = data[key]

        counter = 0
        comp_sentiment_sum = 0
        for datum in full_interview:
            uttr = datum['raw']
            ss = sid.polarity_scores(uttr)
            comp_sentiment_sum += ss['compound']
            counter += 1
        
        if counter != 0:
            average_sentiment = comp_sentiment_sum / counter
        else:
            average_sentiment = 0

        subl_path = os.path.join('data', 'SUBTLEX', 'SUBTLEX.csv')
        dict = get_psycholinguistic_features(full_interview, subl_path)
        dict['average_sentiment'] = average_sentiment

        additional_features = []
        for _key, value in dict.items():
            additional_features.append(value)    

        new_dataframe.append([key] + additional_features)

    final_dataframe = pd.DataFrame(new_dataframe)
    final_dataframe.columns = ['id', 'familiarity', 'concreteness', 'imagability', 'aoa', 'SUBTLFreq', 'average_sentiment']
    final_dataframe.to_csv(os.path.join('data', 'extracted', 'psycholinguistic_info.csv'))

if __name__ == '__main__':
    print('\nPsycholinguistic features extraction started!\n')
    extract_psycholinguistic()
    print('\nPsycholinguistic features extraction finished!\n')
    print('*****************************************************')