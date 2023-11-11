# api.py
import requests
from .image_processing import encode_image, resize_image
from .config import config

def get_compliment(image_path, image_text):
    # Upload the image as a file to OpenAI

    resized_image = resize_image(image_path)
    # Getting the base64 string
    base64_image = encode_image(resized_image)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['api_key']}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": image_text
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
            ]
        }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Process the response to extract the compliment
    compliment = response.json()['choices'][0]['message']['content'].strip()
    return compliment
