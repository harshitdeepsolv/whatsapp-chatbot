import os
import uuid

from pydub import AudioSegment
import requests
import soundfile as sf

from config import config

from openai import OpenAI

client = OpenAI(api_key=config.OPENAI_API_KEY)
def chat_completion(prompt: str) -> str:
    try:

        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a the front face of DeepSolv , an ai based startup focusing on creating industry ready tech for solving their problems.Take Full responsibility for representing the company"},
            {"role": "user", "content": prompt}
        ]
        )

        return response.choices[0].message.content

    except:
        return config.ERROR_MESSAGE
    
def transcript_audio(media_url: str) -> dict:
    try:

        # Download and save the OGG file
        ogg_file_path = f'{config.OUTPUT_DIR}/{uuid.uuid1()}.ogg'
        print(f"path---{ogg_file_path}---")
        data = requests.get(media_url)
        print(data)
        if data.status_code == 200:
            with open(ogg_file_path, 'wb') as file:
                file.write(data.content)
        else:
            raise Exception(f"Failed to download audio. Status code: {data.status_code}")

        # Read the OGG file and save it as MP3 using pydub
        audio = AudioSegment.from_ogg(ogg_file_path)
        mp3_file_path = f'{config.OUTPUT_DIR}/{uuid.uuid1()}.mp3'
        print(f"mp3 file created at {mp3_file_path}")
        audio.export(mp3_file_path, format="mp3")
        audio_file = open(mp3_file_path, 'rb')
        # os.unlink(ogg_file_path)
        # os.unlink(mp3_file_path)
        # Open the MP3 file for transcription
        # with open(mp3_file_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        print(f"transcription done:{transcript}")
        # Unlink files after transcription
        os.unlink(ogg_file_path)
        os.unlink(mp3_file_path)

        return {
            'status': 1,
            'transcript': transcript
        }

    except Exception as e:
        print('Error at transcript_audio...')
        print(e)
        return {
            'status': 0,
            # 'transcript': transcript['text']
        }

