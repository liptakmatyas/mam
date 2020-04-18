import mam
from mam_testlib.file_utils import read_json, sha1_digest

import os

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

    #   TODO    Test that there are no _other_ files in the storage/index

#   TODO    Add second file
#   TODO    Add same file again

