import mam
from mam_testlib.file_utils import read_json

import os

import pytest



def test_with_empty_dir(tmpdir):
    index = mam.core.AssetIndex()
    assert index.root_dir is None
    assert index.metadata is None
    assert index.metadata_file is None
    assert index.is_empty is None
    assert index.asset_count() is None
    assert index.storage_count() is None

    index_root_dir = '{}/index'.format(tmpdir)
    xr_index_metadata_file = '{}/metadata.json'.format(index_root_dir)

    index.root_dir = index_root_dir
    assert index.root_dir == index_root_dir
    assert index.metadata_file == xr_index_metadata_file
    assert index.is_empty
    assert index.asset_count() == 0
    assert index.storage_count() == 0
    assert os.path.isdir(index.root_dir)
    assert os.path.isfile(index.metadata_file)

    metadata = index.metadata
    xr_metadata = {
        'asset_stats': {
            'total_count': 0,
            'storage_count': 0,
        },
    }
    assert metadata == xr_metadata

    metadata_on_disk = read_json(index.metadata_file)
    assert metadata == metadata_on_disk

