# api.py
from openai import OpenAI
import time
from .image_processing import encode_image, resize_image
class Vision:
    def __init__(self):
        self.last_request = {'time': 0}
        self._client = None

    def analyze(self, frames, prompt):
        # Upload the images as files to OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            *self.build_attachments(frames)
                        ]
                    }
                ],
            max_tokens=300
        )
        
        self.last_request = {'time': time.time()}
        # Process the response to extract the message
        content = response.choices[0].message.content.strip()
        return content


    def build_attachments(self, frames):
        attachments = []
        for image_path in frames:
            resized_image = resize_image(image_path)
            # Getting the base64 string
            base64_image = encode_image(resized_image)
            attachments.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
        return attachments

    @property
    def client(self):
        if self._client is None:
            self._client = OpenAI()
        return self._client