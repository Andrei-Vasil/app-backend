import os
import random
import string


def create_topic(topic: str, port: int):
    os.system(f'curl -s localhost:{port}/topic/{topic} -X POST >> /dev/null')

def delete_topic(topic: str, port: int):
    os.system(f'curl -s localhost:{port}/topic/{topic} -X DELETE >> /dev/null')

def subscribe(topic: str, port: int) -> int:
    random_token = ''.join(random.choice([*string.digits, *string.ascii_letters]) for _ in range(10))
    os.system(f'curl -s localhost:{port}/subscription/{topic} -X POST > data/subscription_{random_token}.txt')
    with open(f'data/subscription_{random_token}.txt', 'r+') as f:
        id = int(f.readline())
    os.system(f'rm data/subscription_{random_token}.txt')
    return id

def unsubscribe(topic: str, id: int, port: int):
    os.system(f'curl -s localhost:{port}/subscription/{topic}/{id} -X DELETE >> /dev/null')
