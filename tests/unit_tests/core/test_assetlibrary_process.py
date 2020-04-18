import mam
from mam_testlib.file_utils import read_json, sha1_digest

import os
import pathlib

import pytest


class FooPlugin(mam.core.assetlibrary.PluginBase):
    name = 'foo'
    suffix = '.plugin'
    ext = '.foo'

    def __init__(self, library):
        self._lib = library

    def _op(self, src, dst):
        with open(dst, 'w') as f:
            f.write('bar\n')


def test_with_empty_dir(tmpdir, test_input):
    lib = mam.core.AssetLibrary(tmpdir)
    lib.storage = mam.core.AssetStorage()
    lib.index = mam.core.AssetIndex()
    assert lib.is_empty

    src = test_input('README.md')
    dst_lib_path = 'some/path/inside/the/asset/library/README.md'

    xr_src_sha1 = sha1_digest(src)
    xr_asset_path = lib.storage.asset_path(xr_src_sha1, '.md')
    xr_full_lib_path = '{}/{}'.format(lib.root_dir, dst_lib_path)
    xr_full_storage_path = '{}/{}'.format(lib.storage.root_dir, xr_asset_path)

    asset_id = lib.import_file(src, dst_lib_path)
    assert os.path.isfile(xr_full_lib_path)
    assert os.path.islink(xr_full_lib_path)

    plugin = FooPlugin
    plugin_name = plugin.name
    lib.register_plugin(plugin)

    xr_processed_sha1 = sha1_digest(test_input('README.md{}{}'.format(plugin.suffix, plugin.ext)))
    xr_processed_asset_path = lib.storage.asset_path(xr_processed_sha1, plugin.ext)
    xr_processed_lib_path = '{}{}{}'.format(dst_lib_path, plugin.suffix, plugin.ext)
    xr_processed_full_lib_path = '{}/{}'.format(lib.root_dir, xr_processed_lib_path)
    xr_processed_full_storage_path = '{}/{}'.format(
        lib.storage.root_dir, xr_processed_asset_path)

    processed_asset_id = lib.process_asset(plugin_name, xr_full_lib_path)
    assert processed_asset_id == xr_processed_sha1
    assert lib.asset_count() == 4
    assert lib.storage_count() == 2
    assert os.path.isfile(xr_processed_full_lib_path)
    assert os.path.islink(xr_processed_full_lib_path)
    assert os.path.isfile(xr_processed_full_storage_path)
    assert not os.path.islink(xr_processed_full_storage_path)
    assert lib.storage.asset_id(xr_processed_full_storage_path) == processed_asset_id
    assert lib.storage.asset_id(xr_processed_full_lib_path) == processed_asset_id
    assert str(pathlib.Path(xr_processed_full_lib_path).resolve()) == xr_processed_full_storage_path

