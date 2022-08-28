import os
import pickle
import pandas as pd
from extractors.psycholinguistic import get_all


def extract_psycholinguistic(prj_dir: str):
    print('Psycholinguistic features extraction started!')
    
    # Load the processed data
    inter_pickle_path = os.path.join(prj_dir, 'data', 'pitt_full_interview.pickle')
    with open(inter_pickle_path, "rb") as file:
        data = pickle.load(file)

    new_dataframe = []
    for key in data.keys():
        print('  Processing ' + str(key) + '...')
        # Get a single conversation
        full_interview, label = data[key]

        # Load all the psycholinguistic metrics + word frequency metric
        subl_path = os.path.join(prj_dir, 'data', 'SUBTLEX', 'SUBTLEX.csv')
        path_to_measures = os.path.join(prj_dir, 'managers', 'extractors', 'psycholing_scores')

        # Extract the features
        dict = get_all(full_interview, subl_path, path_to_measures)

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