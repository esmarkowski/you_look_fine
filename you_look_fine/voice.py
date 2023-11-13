from openai import OpenAI
from .logger import logger
import subprocess
import platform
import time

class Voice:
    def __init__(self, output_file):
        self.last_request = {'time': 0}
        self.output_file = output_file
        self._client = None

    def text_to_speech(self, text, voice="fable", model="tts-1"):
        response = self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )

        self.last_request = {'time': time.time()}

        response.stream_to_file(self.output_file)

    def speak(self):
        subprocess.run([self.system_player, self.output_file])


    @property
    def system_player(self):
        if platform.system() == 'Darwin':
            return 'afplay'
        else:
            return 'mpg123'

    @property
    def client(self):
        if self._client is None:
            self._client = OpenAI()
        return self._client

