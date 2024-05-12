import simulate
import workload
import algorithm
import time
import ebpf
from cpu_time import trace_print, update_cpuT
import threading
import struct
import socket
import psutil

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8083
STRUCT_FORMAT = '<100Q'

def unpack_policy(message):
    policy = list(message)
    processed_policy = {}
    for i in range(len(message)):
        priority = message[i] % 1000000
        ts = int((message[i] - priority)/1000000)
        processed_policy[i+1] = [priority, ts]
    return processed_policy

def pack_policy(new_policy):
    packed_policy = []
    for k in range(1, len(new_policy) + 1):
        v = int(new_policy[k][1]) *1000000 + new_policy[k][0]
        packed_policy.append(v)
    return [int(x) for x in packed_policy]

def handle_client(client_socket):
    init = True
    init_v = 0
    while True:
        data = client_socket.recv(struct.calcsize(STRUCT_FORMAT))
        if not data:
            break
        time.sleep(1)
        per_cpu_utilization = psutil.cpu_percent(interval=1, percpu=True)[:24]
        cpu_ulilization = sum(per_cpu_utilization) / len(per_cpu_utilization)
        message = struct.unpack(STRUCT_FORMAT, data)
        
        previous = unpack_policy(message)
        wl, init_v = workload.readWorkload(init, init_v)
        init = False
        simulate.simulate(wl, "srtf", "", timeSlice = 8, period = 2000, CScost = 0)
        new = algorithm.heurtistic(cpu_ulilization, previous)
        new = pack_policy(new)

        response = struct.pack(STRUCT_FORMAT, *new)
        client_socket.send(response)

    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    exp = "/mydata/exp_cpu/test1"
    exp_result = "/root/artifact/iad_huawei_15000_seals_seals_c_1"
    try:
        stop_event = threading.Event()
        thread = threading.Thread(target=trace_print, args=(stop_event,exp,))
        thread.start()
        while True:
            client_socket, addr = server_socket.accept()
            handle_client(client_socket)
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        stop_event.set()
        thread.join()
        update_cpuT(exp, exp_result)
        client_socket.close()
        server_socket.close()


if __name__ == "__main__":
    main()