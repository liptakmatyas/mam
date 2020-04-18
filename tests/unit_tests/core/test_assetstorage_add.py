import mam
from mam_testlib.file_utils import sha1_digest

import os


def test_with_empty_dir(tmpdir, test_input):
    storage_root_dir = "{}/storage".format(tmpdir)
    storage = mam.core.AssetStorage(storage_root_dir)

    src = test_input('README.md')
    xr_src_sha1 = sha1_digest(src)
    xr_src_filesize = os.path.getsize(src)
    xr_src_asset_dir = '/'.join(list(xr_src_sha1[:2]))
    xr_src_asset_filename = xr_src_sha1[2:]
    xr_src_asset_ext = '.md'
    xr_src_asset_path = '{}/{}{}'.format(
        xr_src_asset_dir,
        xr_src_asset_filename,
        xr_src_asset_ext
    )
    xr_src_storage_dir = '{}/{}'.format(storage.root_dir, xr_src_asset_dir)
    xr_src_storage_path = '{}/{}{}'.format(
        xr_src_storage_dir,
        xr_src_asset_filename,
        xr_src_asset_ext
    )

    asset_id, asset_path, storage_path = storage.import_file(src)
    assert asset_id == xr_src_sha1
    assert asset_path == xr_src_asset_path
    assert storage_path == xr_src_storage_path
    assert os.path.isdir(xr_src_storage_dir)
    assert os.path.isfile(storage_path)
    assert os.path.getsize(storage_path) == xr_src_filesize

    #   TODO    Test that there are no _other_ files in the storage

#   TODO    Add second file
#   TODO    Add same file again

