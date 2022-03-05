import os
import pandas as pd
from feature_sets.discourse import get_all

def extract_discours_based():
    dataframe = []
    base_path = os.path.join('data', 'discourse_trees')
    for sub_dir in ['control', 'dementia']:
        data = get_all(os.path.join(base_path, sub_dir))
        for id, feat_dict in data.items():
            new_dict = {'id': id}
            new_dict.update(feat_dict)
            dataframe.append(new_dict)

    dataframe = pd.DataFrame(dataframe)
    dataframe.to_csv(os.path.join('data', 'extracted', 'discourse_info.csv'))

if __name__ == '__main__':
    extract_discours_based()