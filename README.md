# You Look Fine To Me

This Python script, detect_motion.py, is designed to detect motion through a webcam. When motion is detected, it sends a request to an AI assistant, which generates a compliment based on the image captured. The compliment is then converted to speech and played back.

The script accepts several command-line arguments:

--debug: Runs the program in debug mode. In this mode, instead of sending a request to the AI assistant, the program prints a debug message.
--run-once: Makes the program exit after a single request has been made.
The script uses OpenCV for motion detection and the OpenAI API for generating compliments. It's designed to be run on a Mac, using the afplay command to play audio.

The script handles keyboard interrupts, so you can stop it by pressing Ctrl+C. It also ensures that the webcam is properly released and all windows are destroyed when the script ends, regardless of whether it was interrupted or finished normally.


Use at your own risk. You can easily hit rate limits if you don't use --run-once or read the command line arguments. 


```
python detect_motion.py --debug --run-once
```

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/yourrepository.git
```

2. Navigate to the project directory:
```
cd yourepository
```

3. Install the required Python packages:
```
pip install -r requirements.txt
```

4. Set your OpenAI API key as an environment variable:
```
export OPENAI_API_KEY=your_actual_key_here
```


## Usage

Run the script from the command line with the following arguments:

```
python detect_motion.py --repeat-delay 5000 --motion-threshold 10000 --max-time-between-requests 15 --debug
```

## Command-line arguments

- `--repeat-delay`: The delay between repetitions, in milliseconds. Default is 5000.
- `--motion-threshold`: The motion detection threshold. Default is 10000.
- `--max-time-between-requests`: The maximum time between requests, in seconds. Default is 15.
- `--debug`: Enable debug mode. If this flag is present, the program will print a debug message instead of sending a request to the API.
- `--mute`: Mutes TTS.
- `--run-once`: Runs until motion is detected and compliment is delivered. 
- `--vision-prompt TEXT`: Instructions for vision. Default: Give a short compliment based on the person's appearance in the image. Call out distinct features.
- `--voice TEXT`: The voice to use for text-to-speech. Default is 'fable'. Choices are 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'.

# Running

```
python detect_motion.py --repeat-delay 15000 --motion-threshold 10000 --max-time-between-requests 50000
```
