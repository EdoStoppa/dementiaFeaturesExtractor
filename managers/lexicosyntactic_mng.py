import os
import pickle
from pathlib import Path
import pandas as pd
from extractors.pos_phrases import get_all as get_all_phrases
from extractors.pos_syntactic import get_all as get_all_syn

def extract_lexicosyntactic(prj_dir: str):
    print('Lexicosyntactic features extraction started!')
    # Load the preprocessed data
    inter_pickle_path = os.path.join(prj_dir, 'data', 'pitt_full_interview.pickle')
    with open(inter_pickle_path, "rb") as file:
        data = pickle.load(file)

    new_dataframe = []
    for key in data.keys():
        # Get a single conversation
        full_interview, label = data[key]

        print('  Processing ' + key + '...')
        # Extract the features and save them in a dictionary
        lexsyn_dict = {'id': key}
        lexsyn_dict.update(get_all_phrases(full_interview))
        lexsyn_dict.update(get_all_syn(full_interview, prj_dir))

        new_dataframe.append(lexsyn_dict)

    # Create a dataframe using the extracted features
    final_path = os.path.join(prj_dir, 'data', 'extracted', 'lexicosyntactic_info.csv')
    final_df = pd.DataFrame(new_dataframe)

    # Save teh features in a csv file
    final_df.to_csv(final_path, index=False)
    print('Lexicosyntactic features extracted!\n')

if __name__ == '__main__':
    extract_lexicosyntactic(str(Path(__file__).parent[1].absolute()))