import os
from pathlib import Path
import subprocess

import mam


class PluginBase:
    #   These should be defined in the sub-class
    name = None
    suffix = None
    ext = None

    def __init__(self, library):
        self._lib = library

    def run(self, src_full_path):
        asset_id = self._lib.storage.asset_id(src_full_path)
        src_lib_path = self._lib._lib_path_from_path(src_full_path)
        #   TODO    If src is not part of the asset library, import it

        output_lib_path = '{}{}{}'.format(src_lib_path, self.suffix, self.ext)
        output_full_path = self._lib._library_path(output_lib_path)

        self._op(src_full_path, output_full_path)

        return output_full_path, output_lib_path

    def _op(self, src, dst):
        #   The actual operation the plugin performs
        pass


class ShellPluginBase(PluginBase):

    def __init__(self, library):
        super().__init__(library)

    def cmd(self, src, dst):
        #   This should be defined in the sub-class and
        #   it should return the command as a list of strings
        #   (like subprocess.run() expects)
        pass

    def _op(self, src, dst):
        subprocess.run(self.cmd(src, dst))

class AssetLibrary:

    def __init__(self, root_dir):
        self._root_dir = str(root_dir) if root_dir else None

        self._data_dir = "{}/.mam".format(self.root_dir)
        os.makedirs(self.data_dir, exist_ok = True)

        self._storage = None
        self._index = None
        self._plugin = {}

    @property
    def root_dir(self):
        return self._root_dir

    @property
    def data_dir(self):
        return self._data_dir

    @property
    def storage_root_dir(self):
        return "{}/storage".format(self.data_dir)

    @property
    def index_root_dir(self):
        return "{}/index".format(self.data_dir)

    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, storage):
        self._storage = storage
        self.storage.root_dir = self.storage_root_dir

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index
        self.index.root_dir = self.index_root_dir

    @property
    def is_empty(self):
        if not self.index:
            return None
        return self.index.is_empty

    def asset_count(self):
        if not self.index:
            return None
        return self.index.asset_count()

    def storage_count(self):
        if not self.index:
            return None
        return self.index.storage_count()

    def import_file(self, src, dst):
        asset_id, asset_path, storage_path = self.storage.import_file(src)
        self.index.add_entry(asset_id, asset_path, storage_path, src)

        #   FIXME   We should have a general double-check that the file ended
        #           up in the storage. Not just for the in-place import, but
        #           for all imports.

        rel_dst_dir, dst_fn = os.path.split(dst)
        dst_dir = self._library_path(rel_dst_dir)
        library_path = "{}/{}".format(dst_dir, dst_fn)

        if os.path.isfile(library_path):
            #   The file already exists in the library. This means that we need
            #   to do an in-place import: delete the file now, and then the
            #   symlink will be created below.
            os.remove(library_path)
        else:
            #   If the file doesn't exist, the containing directories may be
            #   missing too.
            os.makedirs(dst_dir, exist_ok = True)

        self._link_to_storage(asset_path, storage_path, library_path)

        return asset_id

    def copy_asset(self, src, dst):
        lib_src = self._library_path(src)
        lib_dst = self._library_path(dst)
        lib_dst_dir, _ = os.path.split(lib_dst)
        #   TODO    Error if src/dst extensions are different

        asset_id = self.storage.asset_id(lib_src)
        _, ext = os.path.splitext(lib_src)
        asset_path = self.storage.asset_path(asset_id, ext)
        storage_path = self.storage._storage_path(asset_path)

        os.makedirs(lib_dst_dir, exist_ok = True)
        self._link_to_storage(asset_path, storage_path, lib_dst)

    def process_asset(self, plugin_name, src):
        print("Running plugin '{}({})' ...".format(plugin_name, src))
        plugin = self.plugin(plugin_name)
        output_full_path, output_lib_path = plugin.run(src)

        return self.import_file(output_full_path, output_lib_path)

    def plugin(self, plugin_name):
        return self._plugin[plugin_name](self)

    def register_plugin(self, plugin):
        plugin_name = plugin.name
        self._plugin[plugin_name] = plugin

    def asset_folder(self, asset_id):
        return self.storage._asset_folder(asset_id)

    def asset_file(self, asset_id):
        return self.storage._asset_file(asset_id)

    def _library_path(self, rel_path):
        return "{}/{}".format(self.root_dir, rel_path)

    def _lib_path_from_path(self, path):
        #   TODO    Use the `Path` objects, since they're there... :)
        #           -   Don't create-and-cast-back-to-string every time
        #   FIXME   Check that the path is inside the asset library
        #           -   Now `relative_to()` throws `ValueError`
        return str(Path(path).relative_to(self.root_dir))

    def _link_to_storage(self, asset_path, storage_path, link_path):
        self.index.update_entry_with_new_link(asset_path, new_link = link_path)
        os.symlink(storage_path, link_path)

