import numpy as np

def extract_mean_latency(file_path: str) -> float:
    latency_entries = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            latency_entries.append(float(line))
    return np.mean(latency_entries)

def extract_throughput(file_path: str) -> float:
    throughput_entries = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            throughput_entries.append(line)
    return len(throughput_entries) / (float(throughput_entries[-1]) - float(throughput_entries[0]) + 1)

def extract_total_time(file_path: str) -> dict[str, float]:
    with open(file_path, 'r') as total_time_file:
        producer_line = total_time_file.readline()
        consumer_line = total_time_file.readline()
        return {
            'producer': float(producer_line.split(' ')[-1]),
            'consumer': float(consumer_line.split(' ')[-1])
        }
