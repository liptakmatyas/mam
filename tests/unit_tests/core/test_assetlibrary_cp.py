import mam
from mam_testlib.file_utils import read_json, sha1_digest

import os
import pathlib

import pytest


def test_with_empty_dir(tmpdir, test_input):
    storage = mam.core.AssetStorage()
    index = mam.core.AssetIndex()
    lib = mam.core.AssetLibrary(tmpdir)
    lib.storage = storage
    lib.index = index
    assert lib.is_empty
    assert lib.asset_count() == 0
    assert lib.storage_count() == 0

    src = test_input('README.md')
    dst = 'some/path/inside/the/asset/library/README.md'
    xr_src_sha1 = sha1_digest(src)
    xr_asset_path = lib.storage.asset_path(xr_src_sha1, '.md')
    xr_library_path = '{}/{}'.format(lib.root_dir, dst)
    xr_storage_path = '{}/{}'.format(lib.storage.root_dir, xr_asset_path)

    asset_id = lib.import_file(src, dst)
    assert asset_id == xr_src_sha1
    assert not lib.is_empty
    assert lib.asset_count() == 2
    assert lib.storage_count() == 1
    assert os.path.isfile(xr_library_path)
    assert os.path.islink(xr_library_path)
    assert os.path.isfile(xr_storage_path)
    assert not os.path.islink(xr_storage_path)
    assert lib.storage.asset_id(xr_storage_path) == asset_id
    assert lib.storage.asset_id(xr_library_path) == asset_id

    copy = 'another/path/for/the/same/thing.md'
    xr_copy_library_path = '{}/{}'.format(lib.root_dir, copy)

    lib.copy_asset(dst, copy)
    assert os.path.isfile(xr_copy_library_path)
    assert os.path.islink(xr_copy_library_path)
    assert lib.storage.asset_id(xr_copy_library_path) == asset_id
    assert str(pathlib.Path(xr_copy_library_path).resolve()) == xr_storage_path

