import random
import string

def generate_request(request_size: int) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=request_size))
