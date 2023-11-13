# api.py
import requests
from .image_processing import encode_image, resize_image
from .config import config
from .logger import logger

def get_vision(image_paths, image_text):
    # Upload the images as files to OpenAI

    image_messages = []
    for image_path in image_paths:
        resized_image = resize_image(image_path)
        # Getting the base64 string
        base64_image = encode_image(resized_image)
        image_messages.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })

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
                    *image_messages
                ]
            }
        ],
        "max_tokens": 300
    }

    logger.debug("images: %s", image_paths)

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Process the response to extract the compliment
    compliment = response.json()['choices'][0]['message']['content'].strip()
    return compliment