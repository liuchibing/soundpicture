usage: soundpicture.py [-h] [-i] [-w WINDOW_WIDTH] [-r FRAMERATE] [-v]
                       input_file output_file

Convert a picture to a piece of audio, whose spectrum is the picture.

positional arguments:
  input_file            path to a picture.
  output_file           path to the output. Must be a .wav file.

optional arguments:
  -h, --help            show this help message and exit
  -i, --invert-color    invert color (recommended for light picture).
  -w WINDOW_WIDTH, --window-width WINDOW_WIDTH
                        the width of window when generating spectrum.
  -r FRAMERATE, --framerate FRAMERATE
                        framerate of the output.
  -v, --verbose         enable verbose output.

Copyright 2019 Liu Chibing.
