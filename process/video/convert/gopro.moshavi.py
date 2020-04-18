#!/usr/bin/env python3
"""Convert raw GoPro video file for datamoshing

Usage:
    gopro.moshavi.py <input_file>...
    gopro.moshavi.py --help
    gopro.moshavi.py --version
"""

from docopt import docopt
import subprocess

ext="mosh.avi"

def main(args):
    for input_file in args['<input_file>']:
        output_file = "{}.{}".format(input_file, ext)
        print("Converting", input_file, "to", output_file)

        cmd = [
            "ffmpeg",
            "-i", input_file,

            #   video
            "-vcodec", "libx264",
            "-x264-params", "keyint=9999999:scenecut=0",
            "-qscale:v", "0",

            #   disable audio
            "-an",

            #   bitrate
            "-b:v",     "20000k",
            "-maxrate", "20000k",
            "-bufsize", "10000k",

            #   no B-frames
            "-bf", "0",

            output_file,
        ]

        subprocess.run(cmd)

if __name__ == '__main__':
    args = docopt(__doc__, version='always-alpha')
    main(args)

