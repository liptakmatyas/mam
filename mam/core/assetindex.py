from datetime import datetime
import json
import os


def now():
    return datetime.strftime(datetime.utcnow(), '%Y-%m-%d %H:%M:%S UTC')


class AssetIndex:

    def __init__(self, root_dir = None):
        self._root_dir = None
        self._metadata = None
        self._metadata_file = None

        self.root_dir = root_dir

    @property
    def root_dir(self):
        return self._root_dir

    @root_dir.setter
    def root_dir(self, root_dir):
        self._root_dir = root_dir
        if self.root_dir:
            print("Creating index root dir", self.root_dir)
            os.makedirs(self.root_dir, exist_ok = True)
            self.clear_metadata()

    @property
    def metadata_file(self):
        if not self.root_dir:
            return None
        return "{}/metadata.json".format(self.root_dir)

    @property
    def metadata(self):
        return self._metadata

    def clear_metadata(self):
        self._metadata = {
            'asset_stats': {
                'total_count': 0,
                'storage_count': 0,
            },
        }

        self._write_metadata()

    @property
    def is_empty(self):
        if self.asset_count() is None:
            return None
        return self.asset_count() == 0

    def asset_count(self):
        if self.metadata is None:
            return None
        return self.metadata['asset_stats']['total_count']

    def storage_count(self):
        if self.metadata is None:
            return None
        return self.metadata['asset_stats']['storage_count']

    def add_entry(self, asset_id, asset_path, storage_path, filename):
        #   Create new index entry
        #   FIXME   Consolidate with the PATTERN['timestamp']. Use this, w/o the "%Z"
        timestamp_format = '%Y-%m-%dT%H:%M:%S'
        index_entry = {
            "asset_id": asset_id,
            "original_file": filename,
            "storage_path": storage_path,
            "added_at_utc": datetime.strftime(datetime.utcnow(), timestamp_format),
            "linked_from": [],
        }
        self._write_entry(asset_path, index_entry)

        #   Update index metadata
        self._metadata['asset_stats']['total_count'] += 1
        self._metadata['asset_stats']['storage_count'] += 1
        self._write_metadata()

    def update_entry_with_new_link(self, asset_path, new_link):
        #   Update index entry
        entry = self._read_entry(asset_path)
        entry['linked_from'].append(new_link)
        self._write_entry(asset_path, entry)

        #   Update index metadata
        #   NOTE:   Storage count stays the same due to symlinking
        self._metadata['asset_stats']['total_count'] += 1
        self._write_metadata()

    def _entry_path(self, asset_path, create_folder = False):
        asset_dir, asset_fn = os.path.split(asset_path)
        entry_dir = "{}/{}".format(self.root_dir, asset_dir)
        entry_fn = "{}.index-entry.json".format(asset_fn)
        entry_path = "{}/{}".format(entry_dir, entry_fn)

        if create_folder:
            print("Creating folder", entry_dir)
            os.makedirs(entry_dir, exist_ok = True)

        return entry_path

    def _write_entry(self, asset_path, entry):
        entry_path = self._entry_path(asset_path, create_folder = True)
        with open(entry_path, 'w') as f:
            json.dump(entry, f)

    def _read_entry(self, asset_path):
        entry_path = self._entry_path(asset_path)
        with open(entry_path, 'r') as f:
            return json.load(f)

    def _write_metadata(self):
        if not self.metadata_file or not self.metadata:
            return

        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f)

