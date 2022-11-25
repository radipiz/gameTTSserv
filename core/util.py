import hashlib


def sha1_sum(s: str) -> str:
    hash_func = hashlib.sha1()
    hash_func.update(s.encode())
    return hash_func.hexdigest()


def generate_filename(*args) -> str:
    return sha1_sum('-'.join(map(str, args)))
