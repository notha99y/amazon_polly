from amazon_poly import TTS
from pathlib import Path
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError

session = Session(profile_name="adminuser")
polly = session.client("polly")


list_of_speakers = [
    'Salli',
    'Joanna',
    'Ivy',
    'Kendra',
    'Kimberly',
    'Matthew',
    'Justin',
    'Joey'
]


import random
import string

def get_random_string(length):
    letters = string.ascii_uppercase
    result_str = ' '.join(random.choice(letters) for i in range(length))
    return result_str



if __name__ == "__main__":
    with open('speeches.csv','w') as f:
        f.write('filename,speaker,text\n')
        count = 0
        for i in range(100):
            random_string = get_random_string(4)
            for speaker in list_of_speakers:
                filename = f'speech_{count}.mp3'
                TTS(random_string, speaker, filename)
                f.write(f'{filename},{speaker},{random_string}\n')
                count+=1