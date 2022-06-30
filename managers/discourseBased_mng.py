import os
import pandas as pd
from extractors.discourse import get_all

def extract_discourse_based(prj_dir: str):
    dataframe = []
    base_path = os.path.join(prj_dir, 'data', 'discourse_trees')
    for sub_dir in ['control', 'dementia']:
        data = get_all(os.path.join(base_path, sub_dir))
        for id, feat_dict in data.items():
            print('Processing ' + id + '...')
            new_dict = {'id': id}
            new_dict.update(feat_dict)
            dataframe.append(new_dict)

    final_path = os.path.join(prj_dir, 'data', 'extracted', 'discourse_info.csv')
    final_df = pd.DataFrame(dataframe)
    final_df.to_csv(final_path, index=False)

if __name__ == '__main__':
    print('\nDiscourse-Based features extraction started!\n')
    extract_discourse_based(os.getcwd())
    print('\nDiscourse-Based features extraction finished!\n')
    print('*****************************************************')