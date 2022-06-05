import pandas as pd
import os

def merge_datasets():
    # Generate the path to all partial datasets
    data_dir = os.path.join('.', 'data', 'extracted')
    # Generate a list of datasets names
    file_names = os.listdir(data_dir)
    # Remove the anagraphic info that will be treated later
    file_names.remove('anagraphic_info.csv')

    #################### Create a dataframe with (almost) all the features concatenated ####################
    print('Creating the partial concatenated features dataframe...')

    # Merge (almost) all csv files
    final_dataset = pd.read_csv(os.path.join(data_dir, file_names.pop(0)), index_col=0)
    for file in file_names:
        new_data =  pd.read_csv(os.path.join(data_dir, file), index_col=0)
        print(f'Columns length: {len(new_data.columns)} + {len(final_dataset.columns)} = ' , end='')
        final_dataset = final_dataset.join(new_data, how='inner')
        print(f'{len(final_dataset.columns)}')

    print('Creation complete\n')

    #################### Create the final dataset and save it ####################
    print('Creating the final dataframe...')

    anagraphic = pd.read_csv(os.path.join(data_dir, 'anagraphic_info.csv'), index_col=0)
    final_dataset = anagraphic.join(final_dataset, how='inner')
    final_dataset.to_csv(os.path.join('.', 'data', 'feature_dataset.csv'))

    print('Everything complete!')
    print('Final Dataset:\n')
    print(final_dataset.head())

if __name__ == '__main__':
    merge_datasets()