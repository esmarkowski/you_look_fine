from openai import OpenAI
from .config import config

def text_to_speech(text, output_file):

        # return

    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice=config['voice'],
        input=text
    )

    response.stream_to_file(output_file)
