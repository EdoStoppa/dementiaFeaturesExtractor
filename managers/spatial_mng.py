from extractors.spatial import get_all
import pandas as pd
import pickle
import os

def extract_spatial(prj_dir: str):
    print('Spatial features extraction started!')
    # Load the preprocessed data
    data_path = os.path.join(prj_dir, 'data', 'pitt_full_interview.pickle')
    with open(data_path, "rb") as file:
        data = pickle.load(file)

    final_df = []
    for key in data.keys():
        # Get a single conversation
        full_interview, label = data[key]

        # Extract the features and save them in a dictionary
        print('  Processing ' + key + '...')
        sp_dict = {'id': key}
        for typ in ['halves', 'strips', 'quadrants']:
            sp_dict.update(get_all(full_interview, typ))

        final_df.append(sp_dict)

    # Create a dataframe using the extracted features
    final_path = os.path.join(prj_dir, 'data', 'extracted', 'spatial_info.csv')
    final_df = pd.DataFrame(final_df)

    # Save teh features in a csv file
    final_df.to_csv(final_path, index=False)
    print('Spatial features extracted!\n')

if __name__ == '__main__':
    extract_spatial(os.getcwd())