import os
import pickle
import pandas as pd
from feature_sets.pos_phrases import get_all as get_all_phrases
from feature_sets.pos_syntactic import get_all as get_all_syn

def extract_lexicosyntactic():
    with open(os.path.join('data', 'pitt_full_interview.pickle'), "rb") as file:
        data = pickle.load(file)

    new_dataframe = []
    for key in data.keys():
        full_interview, label = data[key]

        print('\nProcessing ' + key + '...')

        lexsyn_dict = {'id': key}
        lexsyn_dict.update(get_all_phrases(full_interview))
        lexsyn_dict.update(get_all_syn(full_interview))

        new_dataframe.append(lexsyn_dict)

    final_dataframe = pd.DataFrame(new_dataframe)
    final_dataframe.to_csv(os.path.join('data', 'extracted', 'lexicosyntactic_info.csv'))

if __name__ == '__main__':
    extract_lexicosyntactic()