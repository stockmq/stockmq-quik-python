#!/usr/bin/env python3
import threading
import time
import click

from stockmq.rpc import RPCClient


def call(thread_id, uri, n):
    print(f"Thread {thread_id} started")

    with RPCClient(uri) as rpc:
        for i in range(0, n):
            if rpc.call("stockmq_test", i) != i:
                raise Exception("Invalid result")


@click.command()
@click.option("-u", default="tcp://127.0.0.1:8004", help="Host.")
@click.option("-t", default=8, help="Number of threads.")
@click.option("-c", default=125000, help="Number of calls per thread.")
def main(u, t, c):
    """Simple program that benchmarks StockMQ RPC by calling stockmq_test"""
    t0 = time.time()
    threads = []
    calls = 0
    for i in range(1, t+1):
        calls += c
        threads.append(threading.Thread(target=call, args=(i, u, c)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    t1 = time.time() - t0
    print(f"RPS: {calls/t1}")


if __name__ == "__main__":
    main()
