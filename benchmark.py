#!/usr/bin/env python3
import threading
import time
import argparse

from stockmq.rpc import RPCClient


def call(thread_id, uri, n):
    print(f"Thread {thread_id} started")

    with RPCClient(uri) as rpc:
        for i in range(0, n):
            if rpc.call("stockmq_test", i) != i:
                raise Exception("Invalid result")


def main():
    """Simple program that benchmarks StockMQ RPC by calling stockmq_test()"""
    parser = argparse.ArgumentParser(description='StockMQ Benchmark')
    parser.add_argument("uri", type=str, help="Connection URI (example: tcp://127.0.0.1:8004)")
    parser.add_argument("threads", type=int, help="Number of threads", nargs='?', default=8, const=8)
    parser.add_argument("calls", type=int, help="Number of calls per thread", nargs='?', default=125000, const=125000)
    args = parser.parse_args()

    t0 = time.time()
    threads = []
    calls = 0

    for i in range(1, args.threads+1):
        calls += args.calls
        threads.append(threading.Thread(target=call, args=(i, args.uri, args.calls)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    t1 = time.time() - t0
    print(f"Calls: {calls}, Time: {t1}")
    print(f"RPS: {calls/t1}")


if __name__ == "__main__":
    main()
