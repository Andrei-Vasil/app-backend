import json
import os
import time
from extract_data import extract_mean_latency, extract_throughput, extract_total_time
from generate_request import generate_request
from http_client.misc import create_topic, delete_topic, subscribe, unsubscribe
from http_client.publish import publish_multiple
from http_client.receive import receive_multiple

LANGUAGE_TO_PORT = {
    'rust': 5001,
    'c++': 5002,
    'python multithreaded': 5003,
    'python async': 5004
}

CODING_LANGUAGE = {
    'rust': 'rust',
    'c++': 'cpp',
    'python multithreaded': 'pymt',
    'python async': 'pyasync'
}

TOPIC: str = 'topic1'

def process_request(language: str, request: str, no_of_requests: int):
    id = generate_request(15)
    no_of_producers = no_of_clients = 1
    port = LANGUAGE_TO_PORT[language]
    benchmark_file = f'{id}-{CODING_LANGUAGE[language]}.csv'
    file_path = f'{id}.csv'
    with open(f'data/requests/0/{file_path}', 'w') as f:
        f.seek(0)
        json.dump({
            'item': request,
            'benchmark_id': 1
        }, f, indent=4)

    create_topic(TOPIC, port)
    client_ids = [subscribe(TOPIC, port) for _ in range(no_of_clients)]

    t1 = time.time()
    producer_idx = 0    
    publish_multiple(TOPIC, f'data/requests/{producer_idx}/{file_path}', benchmark_file, id, port, no=no_of_requests // no_of_producers, start=producer_idx * (no_of_requests // no_of_producers))    
    os.system(f'echo "Producer {id}-{CODING_LANGUAGE[language]} {no_of_producers}to{no_of_clients} Total time: {time.time() - t1}" >> data/benchmarks/total_time.txt')
    print('finish write', time.time() - t1)

    t2 = time.time()
    for client_id in client_ids:    
        receive_multiple(client_id, TOPIC, benchmark_file, id, port, no=no_of_requests)        
    os.system(f'echo "Consumer {id}-{CODING_LANGUAGE[language]} {no_of_producers}to{no_of_clients} Total time: {time.time() - t2}" >> data/benchmarks/total_time.txt')
    print('finish read', time.time() - t2)

    for client_id in client_ids:
        unsubscribe(TOPIC, client_id, port)
    delete_topic(TOPIC, port)
    print(f'benchmark {id} {no_of_producers}to{no_of_clients} ended')

    total_time = extract_total_time('data/benchmarks/total_time.txt')
    results = {
        'producer': {
            'throughput': extract_throughput(f'data/benchmarks/publish/throughput-{benchmark_file}'),
            'latency': extract_mean_latency(f'data/benchmarks/publish/latency-{benchmark_file}'),
            'total_time': total_time['producer'],
        },
        'consumer': {
            'throughput': extract_throughput(f'data/benchmarks/receive/throughput-{benchmark_file}'),
            'latency': extract_mean_latency(f'data/benchmarks/receive/latency-{benchmark_file}'),
            'total_time': total_time['consumer'],
        }
    }
    os.system(f'rm data/benchmarks/publish/throughput-{benchmark_file}')
    os.system(f'rm data/benchmarks/publish/latency-{benchmark_file}')
    os.system(f'rm data/benchmarks/receive/throughput-{benchmark_file}')
    os.system(f'rm data/benchmarks/receive/latency-{benchmark_file}')
    os.system('rm data/benchmarks/total_time.txt')
    os.system(f'rm data/requests/0/{file_path}')

    return results
