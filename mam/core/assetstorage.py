import hashlib
import os
import shutil


class AssetStorage:
    #   We store the asset files similarly to Git:
    #
    #   -   We have one _storage file_ per `asset_id` containing the original
    #       file contents.
    #   -   The `asset_id` is the basis of the path of this _storage file_.
    #   -   To decrease the maximum number of files/folders per folder, the
    #       first two characters of the `asset_id` are used as nested directory
    #       names and the remaining characters form the filename of the
    #       _storage file_.
    #   -   The extension of the _storage file_ is the extension of the
    #       original file.

    #   The level of nesting in the storage file paths
    _NESTING_LEVEL = 2

    def __init__(self, root_dir = None):
        self.root_dir = root_dir

    @property
    def root_dir(self):
        return self._root_dir

    @root_dir.setter
    def root_dir(self, root_dir):
        self._root_dir = root_dir
        if self.root_dir:
            print("Creating storage root dir", self.root_dir)
            os.makedirs(self.root_dir, exist_ok = True)

    def asset_id(self, filename):
        buf_size = 2**20                # 1 MB
        sha1 = hashlib.sha1()

        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(buf_size)
                if not chunk:
                    break
                sha1.update(chunk)

        return sha1.hexdigest()

    def asset_path(self, asset_id, ext = ''):
        return "{}/{}{}".format(
            self._asset_dir(asset_id),
            self._asset_filename(asset_id),
            ext
        )

    def import_file(self, src):
        asset_id = self.asset_id(src)
        asset_path, storage_path = self._copy_file_into_storage(src, asset_id)

        return asset_id, asset_path, storage_path

    def _copy_file_into_storage(self, filename, asset_id):
        _, ext = os.path.splitext(filename)
        asset_path = self.asset_path(asset_id, ext)
        storage_path = self._storage_path(asset_path, create_folder = True)
        shutil.copyfile(filename, storage_path)

        return asset_path, storage_path

    def _asset_dir(self, asset_id):
        #   Returns:
        #       (str) Nested folders
        #   FIXME   Use proper path manipulation [GLOBALLY]
        return '/'.join(list(asset_id[:self._NESTING_LEVEL]))

    def _asset_filename(self, asset_id):
        #   Returns:
        #       (str) Filename
        return asset_id[self._NESTING_LEVEL:]

    #   FIXME   folder/dir

    def _storage_path(self, asset_path, create_folder = False):
        asset_dir, asset_file = os.path.split(asset_path)
        storage_dir = "{}/{}".format(self.root_dir, asset_dir)
        storage_path = "{}/{}".format(storage_dir, asset_file)

        if create_folder:
            print("Creating folder", storage_dir)
            os.makedirs(storage_dir, exist_ok = True)

        return storage_path

