# Soundpicture.py

Convert a picture to a piece of audio, whose spectrum is the picture. This
tool requires numpy, scipy and pillow installed.

## Setup

```bash
# use pip3 if linux.
$ pip install numpy scipy pillow
```

## Command-line usage

```
$ ./soundpicture.py --help
usage: soundpicture.py [-h] [-i] [-w WINDOW_WIDTH] [-r FRAMERATE] [-v]
                       input_file output_file

Convert a picture to a piece of audio, whose spectrum is the picture. This
tool requires numpy, scipy and pillow installed.

positional arguments:
  input_file            path to a picture.
  output_file           path to the output. Must be a .wav file.

optional arguments:
  -h, --help            show this help message and exit
  -i, --invert-color    invert color (recommended for light picture).
  -w WINDOW_WIDTH, --window-width WINDOW_WIDTH
                        the width of window when generating spectrum. 2048 by
                        default.
  -r FRAMERATE, --framerate FRAMERATE
                        framerate of the output. 48000 by default.
  -v, --verbose         enable verbose cli output.

Copyright 2019 Liu Chibing.
```

For example:
```
$ ./soundpicture.py example.jpg example.wav
```

## Usage as a module
Example:

```python3
import soundpicture

# this module use global variables to store config.
# if you want to use your custom config, use this function.
# DO NOT MODIFY global variables in this module BY HAND.
soundpicture.set_config(window_width=1024, framerate=48000, invert_color=True)

# this function will do all the things needed.
samples = soundpicture.generate("example.jpg", "example.wav")

# feel free to use other functions in this module.
```
