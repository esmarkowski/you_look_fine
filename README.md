# You Look Fine To Me

This Python script, bin/you_look_fine, is designed to detect motion through a webcam. When motion is detected, it sends a request to an AI assistant, which generates a compliment based on the image captured. The compliment is then converted to speech and played back.

__"Mirror, mirror on the wall..."__
```
bin/you_look_fine --debug --run-once
```

The script uses OpenCV for motion detection and the OpenAI API for generating compliments. It's designed to be run on a Mac, Linux (especially raspi), using the afplay or mpg123 command to play audio.

You can stop the script by pressing Ctrl+C. It also ensures that the webcam is properly released and all windows are destroyed when the script ends, regardless of whether it was interrupted or finished normally.

Use at your own risk. You can easily hit rate limits if you don't use --run-once or read the command line arguments. 



## Installation

1. Clone this repository:
```
git clone https://github.com/esmarkowski/you_look_fine.git
```

2. Navigate to the project directory:
```
cd you_look_fine
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
bin/you_look_fine --run-once
```
When running without the `--run-once` argument, the script will continously run and deliver compliments based on the frequency you specify with the following arguments. 

## Command-line arguments

- `--repeat-delay`: The delay between repetitions, in milliseconds. Default is 5000.
- `--motion-threshold`: The motion detection threshold. Default is 10000.
- `--max-time-between-requests`: The maximum time between requests, in seconds. Default is 15.
- `--debug`: Enable debug mode. If this flag is present, the program will print a debug message instead of sending a request to the API.
- `--mute`: Mutes TTS.
- `--run-once`: Runs until motion is detected and compliment is delivered. 
- `--vision-prompt TEXT`: Instructions for vision. Default: Give a short compliment based on the person's appearance in the image. Call out distinct features.
- `--voice TEXT`: The voice to use for text-to-speech. Default is 'fable'. Choices are 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'.

## Examples

#### Run until motion is detected
Useful for testing. The program will run until motion is detected and send a single frame to the OpenAI Vision API, deliver a compliment and exit.

```
bin/you_look_fine --debug --run-once
```

#### Adjust the time between compliments

If you want to send a compliment once every hour, or once a day, and so on then adjust the timing to your liking. This will also determine how frequently request are made to the OpenAI API and can help manage
rate limits and cost. 

```
bin/you_look_fine --repeat-delay 15000 --motion-threshold 10000 --max-time-between-requests 50000
```

#### Adjust the vision prompt
```
bin/you_look_fine --debug --run-once --vision-prompt "Give helpful style advice to the person in the photo. Keep it short, tell them one thing to consider. Address the user as 'You'"
```

#### Visual Assistance
```
bin/you_look_fine --debug --run-once --vision-prompt "You are an assistant for the visually impaired. Describe what's in the image, obstacles and important features. Keep it short."
```

#### Dystopia

```
bin/you_look_fine --debug --run-once --vision-prompt "Describe the person in the image. Keep it short, describe identifying features, age, gender, hair color, tatoos, eye color, etc."
```


## TODO

#### Feature: Infer Action in the scene from multiple frames. 

- Add `--infer-action`, `--capture-frames INT` and `--capture-frames-delay INT`. 
- When `--infer-action` mode is on, capture the number of frames specified by `--capture-frames` spaced apart by `--capture-frames-delay` and send the captured frames to infer action within the scene