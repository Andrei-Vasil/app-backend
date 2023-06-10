import os
import time

def receive_multiple(client_id: int, topic: str, benchmark_file: str, scenario_id: str, port: int, no: int=1):
    for _ in range(no):
        receive(client_id, topic, benchmark_file, scenario_id, port)


def receive(client_id: int, topic: str, benchmark_file: str, scenario_id: str, port: int):
    start = time.time()
    os.system(f'curl -s localhost:{port}/subscription/{topic}/{client_id}/{scenario_id} -X GET >> /dev/null')
    os.system(f'echo {time.time() - start} >> data/benchmarks/receive/latency-{benchmark_file}')
    os.system(f'echo {int(time.time())} >> data/benchmarks/receive/throughput-{benchmark_file}')
