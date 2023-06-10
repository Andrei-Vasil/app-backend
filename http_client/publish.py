import json
import os
import time
import requests

def publish_multiple(topic: str, request_file: str, benchmark_file: str, scenario_id: str, port: int, no: int=1, start: int=0):
    for i in range(start, start + no):
        publish(topic, request_file, benchmark_file, scenario_id, i, port)

def publish(topic: str, request_file: str, benchmark_file: str, scenario_id: str, id: int, port: int):
    with open(request_file, 'r+') as f:
        data = json.load(f)
        data['benchmark_id'] = id
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    start = time.time()
    try:
        with open(request_file, "r") as f:
            body = json.load(f)
            requests.post(f'http://localhost:{port}/publish/{topic}/{scenario_id}', headers={'Content-Type': 'application/json'}, json=body)
    except Exception as e:
        os.system(f'curl -s localhost:{port}/publish/{topic}/{scenario_id} -H "Content-Type: application/json" -X POST -d @{request_file} >> /dev/null')
    os.system(f'echo {time.time() - start} >> data/benchmarks/publish/latency-{benchmark_file}')
    os.system(f'echo {int(time.time())} >> data/benchmarks/publish/throughput-{benchmark_file}')
