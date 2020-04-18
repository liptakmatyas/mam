import mam
from mam_testlib.file_utils import sha1_digest, read_json

import os

import pytest



def test_with_empty_dir(tmpdir, test_input):
    index_root_dir = '{}/index'.format(tmpdir)
    index = mam.core.AssetIndex(index_root_dir)
    assert index.is_empty

    src = test_input('README.md')
    asset_id = sha1_digest(src)
    asset_path = 'asset/path'
    storage_path = '/storage/{}'.format(asset_path)

    xr_index_entry_path = '{}/{}.index-entry.json'.format(
        index.root_dir, asset_path)
    xr_index_entry = {
        'asset_id': asset_id,
        'original_file': src,
        'storage_path': storage_path,
        'added_at_utc': 'TIMESTAMP', # TODO
        'linked_from': [],
    }

    index.add_entry(asset_id, asset_path, storage_path, src)

    assert os.path.isfile(xr_index_entry_path)
    index_entry = read_json(xr_index_entry_path)
    assert index_entry['asset_id'] == xr_index_entry['asset_id']
    assert index_entry['original_file'] == xr_index_entry['original_file']
    assert index_entry['storage_path'] == xr_index_entry['storage_path']
    #   TODO    added_at_utc; pattern match timestamp
    assert index_entry['linked_from'] == xr_index_entry['linked_from']

    metadata = index.metadata
    xr_metadata = {
        'asset_stats': {
            'total_count': 1,
            'storage_count': 1,
        },
    }
    assert metadata == xr_metadata
    assert not index.is_empty
    assert index.asset_count() == 1
    assert index.storage_count() == 1

    metadata_on_disk = read_json(index.metadata_file)
    assert metadata == metadata_on_disk

    link_path = 'link/in/library.md'

    xr_index_entry['linked_from'] = [link_path]

    index.update_entry_with_new_link(asset_path, new_link = link_path)

    index_entry = read_json(xr_index_entry_path)
    assert index_entry['asset_id'] == xr_index_entry['asset_id']
    assert index_entry['original_file'] == xr_index_entry['original_file']
    assert index_entry['storage_path'] == xr_index_entry['storage_path']
    #   TODO    added_at_utc; pattern match timestamp
    assert index_entry['linked_from'] == xr_index_entry['linked_from']

    metadata = index.metadata
    xr_metadata = {
        'asset_stats': {
            'total_count': 2,
            'storage_count': 1,
        },
    }
    assert metadata == xr_metadata
    assert not index.is_empty
    assert index.asset_count() == 2
    assert index.storage_count() == 1

    metadata_on_disk = read_json(index.metadata_file)
    assert metadata == metadata_on_disk

    copy_path = 'another/link/in/library.md'

    xr_index_entry['linked_from'] = [link_path, copy_path]

    index.update_entry_with_new_link(asset_path, new_link = copy_path)

    index_entry = read_json(xr_index_entry_path)
    assert index_entry['asset_id'] == xr_index_entry['asset_id']
    assert index_entry['original_file'] == xr_index_entry['original_file']
    assert index_entry['storage_path'] == xr_index_entry['storage_path']
    #   TODO    added_at_utc; pattern match timestamp
    assert index_entry['linked_from'] == xr_index_entry['linked_from']

    metadata = index.metadata
    xr_metadata = {
        'asset_stats': {
            'total_count': 3,
            'storage_count': 1,
        },
    }
    assert metadata == xr_metadata
    assert not index.is_empty
    assert index.asset_count() == 3
    assert index.storage_count() == 1

    metadata_on_disk = read_json(index.metadata_file)
    assert metadata == metadata_on_disk

    #   TODO    Test that there are no _other_ files in the index

