import json 
import hashlib as hl

def hash_string_256(string):
    return hl.sha256(string).hexdigest()

def hash_block(block):
    """Hashes a block and returns a string representation."""
    return hash_string_256(json.dumps(block, sort_keys=True).encode())
  