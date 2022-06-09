from feature_sets.psycholinguistic import get_spatial_features
import pandas as pd
import pickle
import os

def extract_spatial(prj_dir: str):
    data_path = os.path.join(prj_dir, 'data', 'pitt_full_interview.pickle')
    with open(data_path, "rb") as file:
        data = pickle.load(file)

    final_df = []
    for key in data.keys():
        full_interview, label = data[key]

        print('Processing ' + key + '...')

        sp_dict = {'id': key}
        for typ in ['halves', 'strips', 'quadrants']:
            sp_dict.update(get_spatial_features(full_interview, typ))

        final_df.append(sp_dict)

    final_path = os.path.join(prj_dir, 'data', 'extracted', 'spatial_info.csv')
    final_df = pd.DataFrame(final_df)
    final_df.to_csv(final_path, index=False)

if __name__ == '__main__':
    print('\nSpatial features extraction started!\n')
    extract_spatial(os.getcwd())
    print('\nSpatial features extraction finished!\n')
    print('*****************************************************')