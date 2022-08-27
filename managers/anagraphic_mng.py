import pandas as pd
import pickle
import os

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


'''
#############################################################################
            Main function that extract the anagraphic features
#############################################################################
'''
def extract_anagraphic(prj_dir: str):
    print('Anagraphic features extraction started!')
    # Open the anagraphic data csv
    anagraphic_path = os.path.join(prj_dir, 'data', 'anagraphic_data', 'anagraphic_data.csv')
    df = pd.read_csv(anagraphic_path)

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
    # Create the dataframe with only the useful data
    anagraphic = pd.DataFrame(imputed_dict_list)
    anagraphic = anagraphic.set_index('id')

    # Load the pickle containing the entire processed dataset
    data_path = os.path.join(prj_dir, 'data', 'pitt_full_interview.pickle')
    with open(data_path, 'rb') as file: 
        full_interw_dict = pickle.load(file)
    # Convert dictionary to a list containing the binary classes values
    bin_data = [[id, 1 if data[1] == 'Dementia' else 0] for id, data in full_interw_dict.items()]
    # Create the binary classification dataframe
    bin_class = pd.DataFrame(bin_data, columns=['id', 'bin_class'])
    bin_class = bin_class.set_index('id')
    
    # Do a join to mantain only the conversations for which we have full information
    anagraphic = anagraphic.join(bin_class, how='inner')

    #Reorganize the columns position
    cols = anagraphic.columns.tolist()
    cols = cols[-5:] + cols[:-5]
    final_dataframe = anagraphic[cols]

    # Save the anagraphic info
    final_path = os.path.join(prj_dir, 'data', 'extracted', 'anagraphic_info.csv')
    final_dataframe.to_csv(final_path)
    print('Anagraphic features extracted!\n')

if __name__ == '__main__':
    extract_anagraphic(os.getcwd())