import os
import pandas as pd
from feature_sets.acoustic import get_mfcc_features

# Feature truncated
# TO CHECK : look at https://github.com/jameslyons/python_speech_features/issues/74

def extract_acoustic(prj_dir: str):
    acoustic_path = os.path.join(prj_dir, 'data', 'audio')
    dict_list = []
    for label in ["Control", "Dementia"]:
        for test in ['cookie']:
            for filename in os.listdir(os.path.join(acoustic_path, label, test)):
                if filename.endswith(".wav"):
                    print ("Processing " + filename + '...')
                    wavfile = os.path.join(acoustic_path, label, test, filename)
                    ac_features = get_mfcc_features(wavfile)
                    ac_features['id'] = filename.replace('.wav', '')
                    dict_list.append(ac_features)

    final_dataframe = pd.DataFrame(dict_list)
    cols = final_dataframe.columns.tolist()
    final_dataframe = final_dataframe[cols[-1:] + cols[:-1]]

    final_path = os.path.join(prj_dir, 'data', 'extracted', 'acoustic_info.csv')
    final_dataframe.to_csv(final_path, index=False)

if __name__ == '__main__':
    print('\nAcoustic Data extraction started!\n')
    extract_acoustic(os.getcwd())
    print('\nAcoustic Data extraction finished!\n')
    print('*****************************************************')
