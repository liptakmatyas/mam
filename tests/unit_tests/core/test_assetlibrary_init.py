import mam
from mam_testlib import PATTERN
from mam_testlib.file_utils import read_json

import os

import pytest


class MockAssetStorage:
    def __init__(self):
        self._lib = None

    @property
    def library(self):
        return self._lib

    def attach_to_library(self, library):
        self._lib = library


class MockAssetIndex:
    def __init__(self):
        self._lib = None

    @property
    def library(self):
        return self._lib

    @property
    def root_dir(self):
        return self._lib.index_root_dir

    def attach_to_library(self, library):
        self._lib = library


def test_with_empty_dir(tmpdir):
    #storage = MockAssetStorage()
    #index = MockAssetIndex()

    lib = mam.core.AssetLibrary(tmpdir)
    assert lib.root_dir == tmpdir
    assert lib.data_dir == "{}/.mam".format(lib.root_dir)
    assert os.path.isdir(lib.data_dir)

    assert lib.storage_root_dir == "{}/storage".format(lib.data_dir)
    assert lib.index_root_dir == "{}/index".format(lib.data_dir)

    assert lib.storage is None
    assert lib.index is None
    assert lib.is_empty is None
    assert lib.asset_count() is None
    assert lib.storage_count() is None

    storage = mam.core.AssetStorage()
    lib.storage = storage
    assert lib.storage == storage
    assert lib.storage.root_dir == lib.storage_root_dir
    assert os.path.isdir(lib.storage.root_dir)
    assert lib.index is None
    assert lib.is_empty is None
    assert lib.asset_count() is None
    assert lib.storage_count() is None

    index = mam.core.AssetIndex()
    lib.index = index
    assert lib.storage == storage
    assert lib.index == index
    assert lib.index.root_dir == lib.index_root_dir
    assert os.path.isdir(lib.index.root_dir)
    assert os.path.isfile(lib.index.metadata_file)
    assert lib.is_empty
    assert lib.asset_count() == 0
    assert lib.storage_count() == 0

