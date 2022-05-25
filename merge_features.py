import pandas as pd
import os
import pickle

# Getting basic variables in place
DATA_DIR = os.path.join('.', 'data', 'extracted')
file_names = os.listdir(DATA_DIR)
# Remove the anagraphic info that will be treated later
file_names.remove('anagraphic_info.csv')

#################### Create a dataframe with the binary classification ####################
print('Creating the binary classification dataframe...')

# Load the pickle containing the entire processed dataset
with open(os.path.join('data', 'pitt_full_interview.pickle'), 'rb') as file: 
    full_interw_dict = pickle.load(file)
# Convert dictionary to a list
full_data_list = [[id, 1 if data[1] == 'Dementia' else 0] for id, data in full_interw_dict.items()]
# Create and save the binary classification dataset
bin_class = pd.DataFrame(full_data_list, columns=['id', 'label'])
bin_class = bin_class.set_index('id')

print('Creation complete\n')

#################### Create a dataframe with (almost) all features concatenated ####################
print('Creating the partial concatenated features dataframe...')

# Merge (almost) all csv files
final_dataset = pd.read_csv(os.path.join(DATA_DIR, file_names.pop(0)), index_col=0)
for file in file_names:
    new_data =  pd.read_csv(os.path.join(DATA_DIR, file), index_col=0)
    print(f'Columns length: {len(new_data.columns)} + {len(final_dataset.columns)} = ' , end='')
    final_dataset = final_dataset.join(new_data, how='inner')
    print(f'{len(final_dataset.columns)}')

print('Creation complete\n')

#################### Create a dataframe with anagraphic features ####################
print('Creating the anagraphic dataframe...')

# Loading anagraphic info
anagraphic = pd.read_csv(os.path.join(DATA_DIR, 'anagraphic_info.csv'), index_col=0)
anagraphic = anagraphic.join(bin_class, how='inner')
cols = anagraphic.columns.tolist()
cols = cols[-2:] + cols[:-2]
anagraphic = anagraphic[cols]

print('Creation complete\n')

#################### Create the final dataset and save it ####################

final_dataset = anagraphic.join(final_dataset, how='inner')
final_dataset.to_csv(os.path.join('.', 'data', 'feature_dataset.csv'))

print('Everything complete!')
print('Final Dataset:\n')
print(final_dataset.head())