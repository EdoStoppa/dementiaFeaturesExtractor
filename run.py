import os
import mp3_to_wav
from extractors import preprocess
from extractors import acoustic_ext, anagraphic_ext, discourseBased_ext
from extractors import lexicosyntactic_ext, psycholinguistic_ext, spatial_ext

# To extract all features simply run this file.
# At the end you'll find in data/extracted all the csv.
# Please, run this file in the main directory of the project,
# otherwise some problem amy arise

def extract_features():
    # First preprocess the data
    preprocess.preprocess_data()

    # Convert from mp3 to wav all the audio files
    mp3_to_wav.convert()

    # Extract all features and save them in different csv files
    acoustic_ext.extract_acoustic()
    anagraphic_ext.extract_anagraphic()
    discourseBased_ext.extract_discours_based()
    lexicosyntactic_ext.extract_lexicosyntactic()
    psycholinguistic_ext.extract_psycholinguistic()
    spatial_ext.extract_spatial()

if __name__ == '__main__':
    # Check if the results directory is present, and if not create it
    list_dirs = os.listdir('data')
    if 'extracted' not in list_dirs:
        os.mkdir(os.path.join('data', 'extracted'))
    
    # Start the feature extraction
    extract_features()