import pandas as pd
import os


def extract_anagraphic():
    # Open the anagraphic data csv
    df = pd.read_csv(os.path.join('data', 'anagraphic_data', 'anagraphic_data.csv'))

    imputed_dict_list = []

    visit_dict = {'visit2':1,'visit3':2,'visit4':3,'visit5':4,'visit6':5,'visit7':6}

    
    for index, row in df.iterrows():
        id = str(row['id']).zfill(3)
        print('Extracting ' + id + '...')
        entry_age = int(row['entryage'])
        initial_date = int(row['idate'].split('-')[-1])

        patient_dict = {
            'id': id+'-0',
            'age': entry_age,
            'sex': row['sex'],
            'race': row['race'],
            'education': row['educ'],
            'mmse': row['mms']
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
                    'mmse': row['mms']
                }
                imputed_dict_list.append(patient_dict)

    final_dataframe = pd.DataFrame(imputed_dict_list)
    final_dataframe.to_csv(os.path.join('data', 'extracted', 'anagraphic_info.csv'), index=False)

if __name__ == '__main__':
    print('\nAnagraphic Data extraction started!\n')
    extract_anagraphic()
    print('\nAnagraphic Data extraction finished!\n')
    print('*****************************************************')