import os
import pickle
import pandas as pd

'''
#############################################################################
       Functions needed to map MMSE scores to Dementia Severity levels
#############################################################################
'''
def multiclass3(mmse):
    if   mmse >= 24: return 0
    elif mmse >= 18: return 1
    else:            return 2

def multiclass4(mmse):
    if   mmse >= 26: return 0
    elif mmse >= 19: return 1
    elif mmse >= 10: return 2
    else:            return 3

def multiclass5(mmse):
    if   mmse >= 30: return 0
    elif mmse >= 26: return 1
    elif mmse >= 19: return 2
    elif mmse >= 10: return 3
    else:            return 4

# This parse all the data already available in the csv file + add the mappings for multiclass labels
def parse_partial_anagraphic_data(data_path):
    # Load the full csv file
    df = pd.read_csv(os.path.join(data_path, 'anagraphic_data', 'anagraphic_data.csv'))

    # Mappings between number of visits (string) to int
    visit_dict = {'visit2': 1,'visit3': 2,'visit4': 3,'visit5': 4,'visit6': 5,'visit7': 6}

    # Generate the anagraphic features (missing the bin_class feature)
    imputed_dict_list = []
    for index, row in df.iterrows():
        id = str(row['id']).zfill(3)
        print('  Processing ' + id + '...')
        entry_age = int(row['entryage'])
        initial_date = int(row['idate'].split('-')[-1])

        patient_dict = {
            'id': id + '-0',
            'age': entry_age,
            'sex': row['sex'],
            'race': row['race'],
            'education': row['educ'],
            'mmse': row['mms'],
            'multi_class3': multiclass3(row['mms']),
            'multi_class4': multiclass4(row['mms']),
            'multi_class5': multiclass5(row['mms'])
        }
        imputed_dict_list.append(patient_dict)

        for key in visit_dict.keys():
            if type(row[key]) == str:
                patient_dict = {
                    'id': id + '-' + str(visit_dict[key]),
                    'age': entry_age + int(row[key].split('-')[-1]) - initial_date,
                    'sex': row['sex'],
                    'race': row['race'],
                    'education': row['educ'],
                    'mmse': row['mms'],
                    'multi_class3': multiclass3(row['mms']),
                    'multi_class4': multiclass4(row['mms']),
                    'multi_class5': multiclass5(row['mms'])
                }
                imputed_dict_list.append(patient_dict)

    return imputed_dict_list

# Add the binary classification label using the full data pickle
def complete_data(data_path, imputed_dict_list):
    # Create the dataframe with only the useful data
    anagraphic = pd.DataFrame(imputed_dict_list)
    anagraphic = anagraphic.set_index('id')

    # Load the pickle containing the entire processed dataset
    full_data_path = os.path.join(data_path, 'pitt_full_interview.pickle')
    with open(full_data_path, 'rb') as file: 
        full_interw_dict = pickle.load(file)
    # Convert dictionary to a list containing the binary classes values
    bin_data = [[id, 1 if data[1] == 'Dementia' else 0] for id, data in full_interw_dict.items()]
    # Create the binary classification dataframe
    bin_class = pd.DataFrame(bin_data, columns=['id', 'bin_class'])
    bin_class = bin_class.set_index('id')
    
    # Do a join to mantain only the conversations for which we have full information
    anagraphic = anagraphic.join(bin_class, how='inner')

    return anagraphic

# Reorganazie the columns to improve readability
def reorg_columns(anagraphic):
    #Reorganize the columns position
    cols = anagraphic.columns.tolist()
    cols = cols[-5:] + cols[:-5]
    final_dataframe = anagraphic[cols]

    return final_dataframe

def get_all(data_path):
    
    partial_data = parse_partial_anagraphic_data(data_path)
    
    anagraphic_df = complete_data(data_path, partial_data)

    final_dataframe = reorg_columns(anagraphic_df)

    return final_dataframe