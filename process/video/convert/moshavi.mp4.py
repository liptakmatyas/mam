#!/usr/bin/env python3
"""Convert datamoshing result to .mkv

Usage:
    moshavi.mp4.py <input_file>...
    moshavi.mp4.py --help
    moshavi.mp4.py --version
"""

from docopt import docopt
import subprocess

ext="mp4"

def main(args):
    for input_file in args['<input_file>']:
        output_file = "{}.{}".format(input_file, ext)
        print("Converting", input_file, "to", output_file)

        cmd = [ "ffmpeg",
            "-i", input_file,
            "-strict", "-2",
            output_file,
        ]

        subprocess.run(cmd)

if __name__ == '__main__':
    args = docopt(__doc__, version='always-alpha')
    main(args)

