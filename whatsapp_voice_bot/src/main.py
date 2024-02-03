from flask import Flask, request

from whatsapp_voice_bot.helper.openai_api import chat_completion, transcript_audio
from whatsapp_voice_bot.helper.twilio_api import send_message
from whatsapp_voice_bot.helper.tts import text_to_speech
from config import config
from whatsapp_voice_bot.helper.gcs_upload import upload_to_gcs
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK', 200

@app.route('/twilio', methods=['POST'])
def twilio():
    try:
        data = request.form.to_dict()
        print(data)
        query = data['Body']
        sender_id = data['From']
        print(f'Sender id - {sender_id}')
        # TODO
        # get the user
        # if not create
        # create chat_history from the previous conversations
        # quetion and answer
        if 'MediaUrl0' in data.keys():
            transcript = transcript_audio(data['MediaUrl0'])
            if transcript['status'] == 1:
                print(f'Query - {transcript["transcript"]}')
                response = chat_completion(transcript['transcript'])
            else:
                response = config.ERROR_MESSAGE
        else:
            print(f'Query - {query}')
            response = chat_completion(query)
        print(f'Response - {response}')

        #need to send this to another service which will return audio script
        path= text_to_speech(response)
        print(path)
        # after storing the data in output.ogg we need to put it on gcs
        gcs_blob_name = f'audio_uploaded.mp3'
        # Upload the audio file to GCS and get the public URL
        # Path to the local audio file
        local_audio_path = '/Users/harshitsingh/Documents/Developer/WhatsApp-Chatbot/output.mp3'
        # Google Cloud Storage bucket name
        gcs_bucket_name = 'twilio_space'
        gcs_audio_url = upload_to_gcs(local_audio_path, gcs_bucket_name, gcs_blob_name)
        print(f"gcs audio url: {gcs_audio_url}")
        send_message(sender_id, response,gcs_audio_url )
        print('Message sent.')
    except Exception as e:
        print(e)

    return 'OK', 200
