import mam

import os


def test_with_empty_dir(tmpdir):
    storage_root_dir = "{}/storage".format(tmpdir)
    storage = mam.core.AssetStorage(storage_root_dir)
    assert storage.root_dir == storage_root_dir
    assert os.path.isdir(storage.root_dir)

