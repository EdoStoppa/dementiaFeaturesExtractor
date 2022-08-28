import os
from extractors.anagraphic import get_all

# This manager is extremely simple because the data is already saved in a csv file
def extract_anagraphic(prj_dir: str):
    print('Anagraphic features extraction started!')
    # Define the path to the data folder
    base_path = os.path.join(prj_dir, 'data')
    
    # Get the anagraphic data
    df = get_all(base_path)

    # Save them to a csv file
    out_path = os.path.join(prj_dir, 'data', 'extracted', 'anagraphic_info.csv')
    df.to_csv(out_path)
    print('Anagraphic features extracted!\n')

if __name__ == '__main__':
    extract_anagraphic(os.getcwd())