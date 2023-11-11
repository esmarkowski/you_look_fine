# image_processing.py
from PIL import Image
import base64

def resize_image(image_path, max_size=(800, 600)):
    with Image.open(image_path) as img:
        # Calculate the aspect ratio
        aspect_ratio = img.width / img.height

        # Calculate the new size that respects the aspect ratio
        if img.width > img.height:
            new_width = min(img.width, max_size[0])
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(img.height, max_size[1])
            new_width = int(new_height * aspect_ratio)

        # Resize the image
        img = img.resize((new_width, new_height))

        # Save the resized image to a temporary file
        temp_path = "/tmp/resized_image.jpg"
        img.save(temp_path)
        return temp_path

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
