import hashlib
import subprocess


def sha1_sum(s: str) -> str:
    hash_func = hashlib.sha1()
    hash_func.update(s.encode())
    return hash_func.hexdigest()


def generate_filename(*args) -> str:
    return sha1_sum('-'.join(map(str, args)))


def locate_espeak() -> str:
    p = subprocess.run(["ldconfig -p | grep espeak | cut -d '>' -f 2"], shell=True, check=True, capture_output=True)
    return p.stdout.decode().splitlines()[0].strip()
