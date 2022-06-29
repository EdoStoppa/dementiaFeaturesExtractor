import os
import mp3_to_wav
import merge_data
from pathlib import Path
from extractors import preprocess
from extractors import acoustic_ext, anagraphic_ext, discourseBased_ext
from extractors import lexicosyntactic_ext, psycholinguistic_ext, spatial_ext

# To extract all features simply run this file.
# At the end you'll find in data/extracted all the csv.
# Please, run this file in the main directory of the project,
# otherwise some problem amy arise

def extract_features():
    # Extract the path pointing to the directory containing this file
    prj_dir = str(Path(__file__).parent.absolute())
    print(prj_dir)

    # First preprocess the data
    preprocess.preprocess_data(prj_dir)

    # Convert from mp3 to wav all the audio files
    mp3_to_wav.convert(prj_dir, remove_mp3=False, need_folders=True)

    # Extract all features and save them in different csv files
    acoustic_ext.extract_acoustic(prj_dir)
    anagraphic_ext.extract_anagraphic(prj_dir)
    discourseBased_ext.extract_discourse_based(prj_dir)
    lexicosyntactic_ext.extract_lexicosyntactic(prj_dir)
    psycholinguistic_ext.extract_psycholinguistic(prj_dir)
    spatial_ext.extract_spatial(prj_dir)

    # Merge all datasets into a single csv file
    merge_data.merge_datasets(prj_dir)

if __name__ == '__main__':
    # Check if the results directory is present, and if not create it
    list_dirs = os.listdir('data')
    if 'extracted' not in list_dirs:
        os.mkdir(os.path.join('data', 'extracted'))
    
    # Start the feature extraction
    extract_features()
    print('\nEverything completed!\n')
