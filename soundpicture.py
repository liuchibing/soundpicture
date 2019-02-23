#!env python
# -*- encoding: utf-8 -*-

from PIL import Image, ImageChops
import numpy as np
from scipy import fftpack
import wave

import argparse

# Configs to be set later
WINDOW_WIDTH = -1
SPECT_WIDTH = -1
IMG_WIDTH = -1
FRAMERATE = -1
INVERT_COLOR = False

# Only supports 16-bits now.
SAMPWIDTH = 2

def set_config(*, window_width=2048, framerate=48000, invert_color=False):
    global WINDOW_WIDTH, SPECT_WIDTH, IMG_WIDTH, FRAMERATE, INVERT_COLOR
    WINDOW_WIDTH = window_width
    SPECT_WIDTH = WINDOW_WIDTH // 2
    IMG_WIDTH = SPECT_WIDTH // 2
    FRAMERATE = framerate
    INVERT_COLOR = invert_color

set_config() # init configs

def prepare_img(img):
    img = img.convert('L') # gray-scale
    if INVERT_COLOR:
        img = ImageChops.invert(img)
    img = img.rotate(90, expand=True)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img = img.resize((IMG_WIDTH, int(img.size[1] * (IMG_WIDTH / img.size[0]))))

    return img

def prepare_spectrum(img):
    img = img / 255.0 * (WINDOW_WIDTH / 2)

    spect = np.zeros((img.shape[0], WINDOW_WIDTH), dtype=np.complex128)
    offset = (SPECT_WIDTH - IMG_WIDTH) // 2
    endindex = offset + IMG_WIDTH

    spect[:, offset:endindex] += img

    for i in range(1, SPECT_WIDTH):
        spect[:, WINDOW_WIDTH - i] = spect[:, i].conj()

    return spect

def generate_samples(spect):
    samples = np.zeros_like(spect, dtype=np.float)
    for i in range(samples.shape[0]):
        samples[i] = fftpack.ifft(spect[i]).real

    samples = samples.ravel()

    # scale the value range
    samples /= np.max([np.max(samples), -np.min(samples)])
    samples *= 32767

    return samples.astype(np.int16)

def write_to_wav(samples, output_file):
    f = wave.open(output_file, 'wb')
    f.setframerate(FRAMERATE)
    f.setnchannels(1),
    f.setsampwidth(SAMPWIDTH)
    f.writeframes(samples.tostring())
    f.close()

def generate(input_file, output_file=None):
    if (isinstance(input_file, Image.Image)):
        f = input_file
    else:
        f = Image.open(input_file)

    img = prepare_img(f)

    img = np.asarray(img)
    spect = prepare_spectrum(img)

    samples = generate_samples(spect)

    if output_file:
        write_to_wav(samples, output_file)

    return samples

def _main():
    parser = argparse.ArgumentParser(prog="soundpicture.py", description="Convert a picture to a piece of audio, whose spectrum is the picture. This tool requires numpy, scipy a", epilog='Copyright 2019 Liu Chibing.')
    parser.add_argument('input_file', help='path to a picture.')
    parser.add_argument('output_file', help='path to the output. Must be a .wav file.')
    parser.add_argument('-i', '--invert-color', action='store_true', help='invert color (recommended for light picture).')
    parser.add_argument('-w', '--window-width', type=int, help='the width of window when generating spectrum.')
    parser.add_argument('-r', '--framerate', type=int, help='framerate of the output.')
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output.')

    opt = parser.parse_args()

    config = dict()
    if opt.window_width:
        config['window_width'] = opt.window_width
    if opt.framerate:
        config['framerate'] = opt.framerate
    if opt.invert_color:
        config['invert_color'] = opt.invert_color
    if len(config):
        set_config(**config)
        print('Using custom config from command line.')

    if opt.verbose:
        print('input: {}\noutput: {}\ninvert color: {}\nwindow width: {}\nframerate: {}'.format(
            opt.input_file, opt.output_file, INVERT_COLOR,
            WINDOW_WIDTH, FRAMERATE
        ))

    generate(opt.input_file, opt.output_file)

    if opt.verbose:
        print('\nWrote {} successfully.'.format(opt.output_file))

if __name__ == '__main__':
    _main()
