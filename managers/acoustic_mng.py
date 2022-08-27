import os
import pandas as pd
from extractors.acoustic import get_mfcc_features

# Feature truncated
# TO CHECK : look at https://github.com/jameslyons/python_speech_features/issues/74

def extract_acoustic(prj_dir: str):
    print('Acoustic features extraction started!')
    # Define the path to the audio files
    acoustic_path = os.path.join(prj_dir, 'data', 'audio')
    # Start going through the files
    dict_list = []
    for label in ["Control", "Dementia"]:
        for test in ['cookie']:
            for filename in os.listdir(os.path.join(acoustic_path, label, test)):
                if filename.endswith(".wav"):
                    print ("  Processing " + filename + '...')
                    # Generate the full path to the wav file
                    wavfile = os.path.join(acoustic_path, label, test, filename)
                    # Extract the features
                    ac_features = get_mfcc_features(wavfile)
                    # Remove the format substring from the id
                    ac_features['id'] = filename.replace('.wav', '')
                    dict_list.append(ac_features)

    # Create a dataframe using the extracted features
    final_dataframe = pd.DataFrame(dict_list)
    cols = final_dataframe.columns.tolist()
    final_dataframe = final_dataframe[cols[-1:] + cols[:-1]]

    # Save the data as a csv file
    final_path = os.path.join(prj_dir, 'data', 'extracted', 'acoustic_info.csv')
    final_dataframe.to_csv(final_path, index=False)
    print('Acoustic features extracted!\n')

if __name__ == '__main__':
    extract_acoustic(os.getcwd())