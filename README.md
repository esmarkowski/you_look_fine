# You Look Fine To Me

This script is designed to detect motion through a video feed and analyze it using GPT Vision and speak the response with OpenAI Text to Speech. It can also be used to infer action over a series of frames. 
It uses OpenCV for motion detection and can filter on object detection (e.g. only sending requests to GPT Vision when a person is detected)

__"Mirror, mirror on the wall..."__
```
bin/you_look_fine --debug --run-once --vision-prompt "Mirror, mirror on the wall.. Describe the person you see. Respond as the mirror from Snow White." --detect person
```

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
bin/you_look_fine --debug --run-once
```
When running without the `--run-once` argument, the script will continously run and deliver compliments based on the frequency you specify with the following arguments. 

## Command-line arguments

- `--motion-threshold`: The motion detection threshold. Default is 10000.
- `--max-time-between-requests`: The maximum time between requests, in milliseconds. Default is 500000.
- `--debug`: Enable debug mode. If this flag is present, the program will run in debug mode.
- `--mute`: Mutes the audio. If this flag is present, the program will run without audio.
- `--run-once`: Runs until detection is made and compliment is given. If this flag is present, the program will exit after one detection and compliment.
- `--vision-prompt`: Instructions for vision. Default: "Give a short compliment based on the person's appearance in the image. Call out distinct features."
- `--voice`: The voice to use for text-to-speech. Default is 'fable'. Choices are 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'.
- `--infer-action`: Infer action in the scene from multiple frames. If this flag is present, the program will infer actions.
- `--capture-frames`: The number of frames to capture when inferring action. Default is 1.
- `--capture-frames-delay`: The delay between capturing frames, in milliseconds. Default is 1000.
- `--camera`: The camera source. Can be an integer for a local camera or a string for an RTSP URL. Default is 0.
- `--soft-run`: Skips making calls to AI
- `--detect`: The features to detect before sending to AI. Choices are one or more of person, car, cat, dog, bird, horse, sheep, cow. Seperated by space.

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
bin/you_look_fine --infer-action --run-once --vision-prompt "You are an assistant for the visually impaired. Describe what's in the image, obstacles and important features. Keep it short."
```

#### Infer Action

```
bin/you_look_fine --debug --run-once --infer-action --capture-frames 3 --capture-frames-delay 1000 --vision-prompt "Please provide a specific description of the action being observed in a single, cohesive moment, using clear and simple language suitable for a 10-year-old. Describe the setting or context and the subjects involved as they appear at one specific instance, not as a sequence of actions. Use precise and descriptive language to capture the nature of the key action in this single moment. The details should be those that can be confidently observed or inferred from this moment. Focus on the most relevant and significant aspects of the action or scene, and respond in second person perspective in one or two sentences."
```

#### Dystopia

```
bin/you_look_fine --debug --run-once --vision-prompt "Describe the person in the image. Keep it short, describe identifying features, age, gender, hair color, tatoos, eye color, etc."
```

#### RTSPS
```
bin/you_look_fine --run-once --infer-action --vision-prompt "Describe who is at the door." --camera "rtsps://YOUR_RTSPS_STREAM"
```

#### Every 30 seconds describe the person or cat
```
bin/you_look_fine --debug --capture-frames 3 --capture-frames-delay 600 --motion-threshold 480000 --camera rtsps://YOUR_RTSP_STREAM --vision-prompt "Please describe the person in this scene. Describe them like you're a surprised hippy. Focus on the most relevant and significant aspects of the person and their outfit, and respond in second person perspective in one or two sentences."  --max-time-between-requests 30000 --detect person cat
```
