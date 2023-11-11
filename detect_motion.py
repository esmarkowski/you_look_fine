import argparse
import cv2
import requests
import json
import subprocess
import os
import base64
import platform
from pathlib import Path
from openai import OpenAI
from PIL import Image

client = OpenAI()

def resize_image(image_path, size=(800, 600)):
    with Image.open(image_path) as img:
        # Resize the image
        img = img.resize(size)

        # Save the resized image to a temporary file
        temp_path = "/tmp/resized_image.jpg"
        img.save(temp_path)
        return temp_path
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to get a compliment based on the person's appearance in the image
def get_compliment(image_path, image_text):
    # Upload the image as a file to OpenAI

    resized_image = resize_image(image_path)
    # Getting the base64 string
    base64_image = encode_image(resized_image)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
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

# Function to convert text to speech
def text_to_speech(text, output_file):
    if debug:
        print("Debug: text_to_speech called with text =", text)
        # return

    response = client.audio.speech.create(
        model="tts-1",
        voice=args.voice,
        input=text
    )

    response.stream_to_file(output_file)


# Parse command-line arguments
parser = argparse.ArgumentParser(description='Run the OpenAI Assistant.')
parser.add_argument('--repeat-delay', type=int, default=5000, help='The delay between repetitions, in milliseconds.')
parser.add_argument('--motion-threshold', type=int, default=10000, help='The motion detection threshold.')
parser.add_argument('--max-time-between-requests', type=int, default=500000, help='The maximum time between requests, in seconds.')
parser.add_argument('--debug', action='store_true', help='Enable debug mode.')
parser.add_argument('--mute', action='store_true', help='Mute audio.')
parser.add_argument('--run-once', action='store_true', help='Runs until detection is made and compliment is given.')
parser.add_argument('--vision-prompt', type=str, default="Give a short compliment based on the person's appearance in the image. Call out distinct features.", help='Instructions for vision.')
parser.add_argument('--voice', type=str, default='fable', choices=['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'], help='The voice to use for text-to-speech.')
args = parser.parse_args()

# Use the arguments in your code
repeat_delay = args.repeat_delay
motion_threshold = args.motion_threshold
max_time_between_requests = args.max_time_between_requests
debug = args.debug
muted = args.mute
run_once = args.run_once
vision_prompt = args.vision_prompt
# Get the API key from the environment
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the motion detection
camera = cv2.VideoCapture(0)  # Use the correct camera index
motion_detector = cv2.createBackgroundSubtractorMOG2()

if debug:
    print("Debug: Beginning")
# Initialize the request state
frame_counter = 0
request_in_progress = False
camera_warmed_up = False

try:
    while True:
        ret, frame = camera.read()
        if not camera_warmed_up:
            frame_counter += 1
            if frame_counter > 20:
                # After 20 frames, consider the camera warmed up
                print("Camera initialized")
                camera_warmed_up = True
            else:
                # Skip this frame and go to the next iteration of the loop
                continue
        if not ret:
            break

        # Apply the motion detector to the frame
        motion_mask = motion_detector.apply(frame)
        
        # If there's enough motion and no request is in progress, proceed
        if motion_mask.sum() > motion_threshold and not request_in_progress:
            
            print("Motion detected")
            # Set the request state to in progress
            request_in_progress = True

            # Save the frame as an image
            image_path = '/tmp/detected_motion.jpg'
            cv2.imwrite(image_path, frame)
            
            # Get a compliment for the image
            compliment = get_compliment(image_path, vision_prompt)
            
            if debug:
                print("Debug: Compliment =", compliment)
            # Convert the compliment to speech
            audio_file = '/tmp/compliment.mp3'
            text_to_speech(compliment, audio_file)
            
            # Play the audio file
            if not muted:
                if platform.system() == 'Darwin':
                    subprocess.run(["afplay", audio_file])
                else:
                    subprocess.run(["mpg123", audio_file])

            # Set the request state back to not in progress
            request_in_progress = False

            if run_once:
                break

            # Wait for a while before detecting motion again to avoid repeats
            cv2.waitKey(repeat_delay)

        # Wait for a while before the next frame
        cv2.waitKey(max_time_between_requests)   
    # Release the camera and close any open windows
except KeyboardInterrupt:
    print("Interrupted by user. Exiting...")
finally:
    # Release the camera and destroy all windows
    camera.release()
    cv2.destroyAllWindows()
