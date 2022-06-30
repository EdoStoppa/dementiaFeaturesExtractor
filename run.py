import os
import mp3_to_wav
import merge_data
from pathlib import Path
from managers import preprocess
from managers import acoustic_mng, anagraphic_mng, lexicosyntactic_mng
from managers import discourseBased_mng, psycholinguistic_mng, spatial_mng

# To extract all features simply run this file.
# At the end you'll find in data/extracted all the csv.
# Please, run this file in the main directory of the project,
# otherwise some problem amy arise

def extract_features(prj_dir: str) -> None:
    # First preprocess the data
    preprocess.preprocess_data(prj_dir)

    # Convert from mp3 to wav all the audio files
    mp3_to_wav.convert(prj_dir, remove_mp3=False, need_folders=True)

    # Extract all features and save them in different csv files
    acoustic_mng.extract_acoustic(prj_dir)
    anagraphic_mng.extract_anagraphic(prj_dir)
    discourseBased_mng.extract_discourse_based(prj_dir)
    lexicosyntactic_mng.extract_lexicosyntactic(prj_dir)
    psycholinguistic_mng.extract_psycholinguistic(prj_dir)
    spatial_mng.extract_spatial(prj_dir)

    # Merge all datasets into a single csv file
    merge_data.merge_datasets(prj_dir)

if __name__ == '__main__':
    # Extract the path pointing to the directory containing this file
    prj_dir = str(Path(__file__).parent.absolute())

    # Check if the results directory is present, and if not create it
    list_dirs = os.listdir(os.path.join(prj_dir, 'data'))
    if 'extracted' not in list_dirs:
        os.mkdir(os.path.join('data', 'extracted'))

    # Start the feature extraction
    import datetime, numpy as np
    millisec = []
    for _ in range(10):
        start = datetime.datetime.now()
        extract_features(prj_dir)
        end = datetime.datetime.now()
        millisec.append((end-start).total_seconds())
        print(f'Iteration {_} complete!\n')
    print(f'\n\nMean time: {round(np.mean(millisec), 3)}s, Stdev: {round(np.std(millisec), 3)}s')
    print('\nEverything completed!\n')
