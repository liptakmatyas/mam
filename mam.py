#!/usr/bin/env python3
"""Media Asset Manager

Usage:
    mam add FROM TO
    mam cp FROM TO
    mam process PLUGIN ASSET
    mam --help
    mam --version

Options:
    --help, -h                      show this help
    --version                       show version
"""
#   TODO    Rename `add` to `import`

from docopt import docopt

import mam

VERSION = '0.0.1'


def main(args):
    lib_root = '.'
    lib = mam.core.AssetLibrary(lib_root)
    lib.storage = mam.core.AssetStorage()
    lib.index = mam.core.AssetIndex()

    lib.register_plugin(mam.plugin.video.Reverse)
    lib.register_plugin(mam.plugin.video.convert.GoproMoshavi)
    lib.register_plugin(mam.plugin.video.convert.MoshaviMp4)

    if args['add']:
        lib.import_file(args['FROM'], args['TO'])
        return

    if args['cp']:
        lib.copy_asset(args['FROM'], args['TO'])
        return

    if args['process']:
        lib.process_asset(args['PLUGIN'], args['ASSET'])


if __name__ == '__main__':
    args = docopt(__doc__, version=VERSION)
    main(args)

