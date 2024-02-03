from gtts import gTTS
from pydub import AudioSegment
from io import BytesIO

def text_to_speech(text, language='en', output_file='output.mp3'):
    """
    Convert text to speech and save it as an MP3 file.

    Parameters:
    - text (str): The text to be converted to speech.
    - language (str): The language of the text (default is English).
    - output_file (str): The name of the MP3 file to be saved (default is 'output.mp3').

    Returns:
    - output_file (str): The name of the generated MP3 file.
    """
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False)

    # Convert gTTS object to MP3 using pydub
    mp3_data = BytesIO()
    tts.write_to_fp(mp3_data)
    mp3_data.seek(0)
    audio = AudioSegment.from_mp3(mp3_data)

    # Save the MP3 file
    audio.export(output_file, format="mp3")

    return output_file

# Example usage:
text = "Hello, this is a test. I hope this script works for you!"
output_file = text_to_speech(text, language='en', output_file='output.mp3')
print(f"Speech saved to {output_file}")
