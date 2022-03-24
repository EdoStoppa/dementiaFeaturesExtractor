import os
import pandas as pd
from feature_sets.discourse import get_all

def extract_discourse_based():
    dataframe = []
    base_path = os.path.join('data', 'discourse_trees')
    for sub_dir in ['control', 'dementia']:
        data = get_all(os.path.join(base_path, sub_dir))
        for id, feat_dict in data.items():
            print('Processing ' + id + '...')
            new_dict = {'id': id}
            new_dict.update(feat_dict)
            dataframe.append(new_dict)

    dataframe = pd.DataFrame(dataframe)
    dataframe.to_csv(os.path.join('data', 'extracted', 'discourse_info.csv'), index=False)

if __name__ == '__main__':
    print('\nDiscourse-Based features extraction started!\n')
    extract_discourse_based()
    print('\nDiscourse-Based features extraction finished!\n')
    print('*****************************************************')