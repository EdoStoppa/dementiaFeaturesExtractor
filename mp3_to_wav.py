import os
from pydub import AudioSegment

def convert():
    # Create empty folders with the correct 
    create_folders()
    mp3_dir = os.path.join('data', 'audiomp3')
    wav_dir = os.path.join('data', 'audio')

    for section in ['Control', 'Dementia']:
        for test in ['cookie', 'fluency', 'recall', 'sentence']:
            path = os.path.join(mp3_dir, section, test)
            audio_files = list(filter(lambda file_name: file_name.endswith('.mp3'), os.listdir(path)))

            for file in audio_files:
                print(os.path.join(section, test, file))
                sound = AudioSegment.from_mp3(os.path.join(mp3_dir, section, test, file))
                sound.export(os.path.join(wav_dir, section, test, file.replace('.mp3', '.wav')), format="wav")

def create_folders():
    base = os.path.join(os.getcwd(), 'data')
    dirs = os.listdir(base)
    if 'audio' not in dirs:
        audio_path = os.path.join(base, 'audio')
        os.mkdir(audio_path)
        for section in ['Control', 'Dementia']:
            sect_path = os.path.join(audio_path, section)
            os.mkdir(sect_path)
            for test in ['cookie', 'fluency', 'recall', 'sentence']:
                os.mkdir(os.path.join(sect_path, test))

if __name__ =='__main__':
    convert()