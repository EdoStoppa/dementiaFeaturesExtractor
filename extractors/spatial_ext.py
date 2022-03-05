from feature_sets.psycholinguistic import get_spatial_features
import pandas as pd
import pickle
import os

def extract_spatial():
    data_path = os.path.join('data', 'pitt_full_interview.pickle')
    with open(data_path, "rb") as file:
        data = pickle.load(file)

    final_dataframe = []
    for key in data.keys():
        full_interview, label = data[key]

        print('Processing ' + key + '...')

        sp_dict = {'id': key}
        for typ in ['halves', 'strips', 'quadrants']:
            sp_dict.update(get_spatial_features(full_interview, typ))

        final_dataframe.append(sp_dict)

    final_dataframe = pd.DataFrame(final_dataframe)
    final_dataframe.to_csv(os.path.join('data', 'extracted', 'spatial_info.csv'))

if __name__ == '__main__':
    extract_spatial()