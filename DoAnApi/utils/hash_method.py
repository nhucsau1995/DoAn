import hashlib


def hash_sha256(base_string):
    return hashlib.sha256(base_string.encode('utf-8')).hexdigest()