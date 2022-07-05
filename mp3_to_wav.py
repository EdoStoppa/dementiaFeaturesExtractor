import os
from pydub import AudioSegment

# need_folders: True if you've not already created the folders for the audio wav files
# remove_mp3: True if you want to delete the file mp3 immediately after the wav conversion (saves space)

def convert(prj_dir: str, need_folders: bool = True, remove_mp3: bool = False):
    # Create empty folders with the correct structure
    if need_folders: create_folders(prj_dir)
    mp3_dir = os.path.join(prj_dir, 'data', 'audiomp3')
    wav_dir = os.path.join(prj_dir, 'data', 'audio')

    for section in ['Control', 'Dementia']:
        for test in ['cookie']:
            # Generate the complete directory path
            dir_path = os.path.join(mp3_dir, section, test)
            # Get all mp3 file names
            audio_files = list(filter(lambda file_name: file_name.endswith('.mp3'), os.listdir(dir_path)))

            for file in audio_files:
                print('Converting ' + str(file) + '...')
                # Generate complete file path
                mp3_path = os.path.join(dir_path, file)
                # Load the mp3 file
                sound = AudioSegment.from_mp3(mp3_path)
                # Convert it to wav and save it
                sound.export(os.path.join(wav_dir, section, test, file.replace('.mp3', '.wav')), format="wav")
                # If option enable, simply delete the old mp3 file
                if remove_mp3: os.remove(mp3_path)

def create_folders(prj_dir: str):
    base = os.path.join(prj_dir, 'data')
    dirs = os.listdir(base)
    if 'audio' not in dirs:
        audio_path = os.path.join(base, 'audio')
        os.mkdir(audio_path)

    audio_path = os.path.join(base, 'audio')
    if 'Control' not in os.listdir(audio_path):
        sect_path = os.path.join(audio_path, 'Control')
        os.mkdir(sect_path)
    if 'Dementia' not in os.listdir(audio_path):
        sect_path = os.path.join(audio_path, 'Dementia')
        os.mkdir(sect_path)
    
    ctrl = os.path.join(audio_path, 'Control')
    dmt = os.path.join(audio_path, 'Dementia')
    if 'cookie' not in  os.listdir(ctrl):
        os.mkdir(os.path.join(ctrl, 'cookie'))
    if 'cookie' not in  os.listdir(dmt):
        os.mkdir(os.path.join(dmt, 'cookie'))


if __name__ =='__main__':
    print('\nMp3 to Wav conversion started!\n')
    convert(os.getcwd(), need_folders=True, remove_mp3=False)
    print('\nMp3 to Wav conversion finished!\n')
    print('*****************************************************')