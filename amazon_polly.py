"""Getting Started Example for Python 2.7+/3.3+"""
import argparse
import os
import subprocess
import sys
import random
from contextlib import closing
from pathlib import Path
from tempfile import gettempdir

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="mac_shopee")
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

def TTS(text, speaker, save_name):
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(
            Text=text, OutputFormat="mp3", VoiceId=speaker
        )
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(os.getcwd(), 'validation_set', save_name)

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

    # Play the audio using the platform's default player
    # if sys.platform == "win32":
    #     os.startfile(output)
    # else:
    #     # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
    #     opener = "open" if sys.platform == "darwin" else "xdg-open"
    #     subprocess.call([opener, output])

if __name__ == "__main__":
    # list_of_speeches = sorted(list(Path('speeches').glob('*.mp3')), key=lambda x: int(x.stem.split('speech')[-1]))
    # START_NUM = int(list_of_speeches[-1].stem.split('speech')[-1]) + 1
    START_NUM=0
    parser = argparse.ArgumentParser('Generate TTS using Amazon Polly')
    parser.add_argument('--speaker', help='Select Speaker')
    parser.add_argument('--start_num', help='Starting number to be appended to the speech to be saved', default=START_NUM)
    parser.add_argument('--end_num', help='Ending number to be appended to the speech to be saved', default=START_NUM + 1)
    parser.add_argument('--text', help='Text to convert to speech')
    args = parser.parse_args()
    
    speaker = args.speaker
    start_num = int(args.start_num)
    end_num = int(args.end_num)
    if speaker:
        assert speaker in list_of_speakers
    else:
        print('No speaker given, randomly selecting a speaker')
        speaker = random.choice(list_of_speakers)
        print('Speaker choosen: ', speaker)
    
    if args.text:
        print('TTS: ', args.text)
        assert end_num - start_num == 1 
        save_name = 'speech' + str(start_num) + '.mp3'
        TTS(args.text, speaker, save_name)

    else:
        reference_texts = Path('texts') / 'reference_texts.txt'
        print('No text given')
        print('Reading from ', str(reference_texts))
        with open(reference_texts, 'r') as f:
            texts = f.readlines()
        assert len(texts) > (end_num - start_num ), 'Too little text in reference text'
        with open('validation_set/validation_meta.csv', 'w') as f:
            f.write('text,speaker,file_name\n')
            for i in range(start_num, end_num + 1):
                print(i)
                text = texts[i - start_num].strip()
                print('TTS: ', text)
                speaker = random.choice(list_of_speakers)
                print('Speaker choosen: ', speaker)
                save_name = 'speech' + str(i) + '.mp3'
                TTS(text, speaker, save_name)
                f.write('{},{},{}\n'.format(text, speaker, save_name))
