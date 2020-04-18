import hashlib
import json


def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def sha1_digest(filename):
    buf_size = 2**20 # 1 MB
    sha1 = hashlib.sha1()

    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(buf_size)
            if not chunk:
                break
            sha1.update(chunk)

    return sha1.hexdigest()

def same_file_content(filename_a, filename_b):
    #   If they have the same digest, they're _probably_ the same
    return sha1_digest(filename_a) == sha1_digest(filename_b)

