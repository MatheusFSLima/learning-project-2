import hashlib

def hash_password(password):
    password_bytes = password.encode()
    hash_object = hashlib.sha256(password_bytes)
    password_hash = hash_object.hexdigest()
    return password_hash