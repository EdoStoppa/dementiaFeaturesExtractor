from extractors.psycholinguistic import get_psycholinguistic_features
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import pickle
import os

def extract_psycholinguistic(prj_dir: str):
    print('Psycholinguistic features extraction started!')
    sid = SentimentIntensityAnalyzer()
    
    # Load the processed data
    inter_pickle_path = os.path.join(prj_dir, 'data', 'pitt_full_interview.pickle')
    with open(inter_pickle_path, "rb") as file:
        data = pickle.load(file)

    new_dataframe = []
    for key in data.keys():
        print('  Processing ' + str(key) + '...')
        # Get a single conversation
        full_interview, label = data[key]

        # Compute the average sentiment of the conversation
        comp_sentiment_sum = 0
        for datum in full_interview:
            uttr = datum['raw']
            ss = sid.polarity_scores(uttr)
            comp_sentiment_sum += ss['compound']
        average_sentiment = 0 if len(full_interview) == 0 else (comp_sentiment_sum / len(full_interview))

        # Load all the psycholinguistic metrics + word frequency metric
        subl_path = os.path.join(prj_dir, 'data', 'SUBTLEX', 'SUBTLEX.csv')
        path_to_measures = os.path.join(prj_dir, 'managers', 'extractors', 'psycholing_scores')

        # Extract the features
        dict = get_psycholinguistic_features(full_interview, subl_path, path_to_measures)
        dict['average_sentiment'] = average_sentiment

        # Format the features
        additional_features = []
        for _key, value in dict.items():
            additional_features.append(value)    

        # Save the features
        new_dataframe.append([key] + additional_features)

    # Create a dataframe with the extracted features
    final_path = os.path.join(prj_dir, 'data', 'extracted', 'psycholinguistic_info.csv')
    final_df = pd.DataFrame(new_dataframe)
    final_df.columns = ['id', 'familiarity', 'concreteness', 'imagability', 'aoa', 'SUBTLFreq', 'average_sentiment']

    # Save to a csv file everything
    final_df.to_csv(final_path, index=False)
    print('Psycholinguistic features extracted!\n')

if __name__ == '__main__':
    extract_psycholinguistic(os.getcwd())