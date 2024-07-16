#!/usr/bin/env python3
import argparse
from stockmq.rpc import RPCClient
from stockmq.rpc import RPCRuntimeError
from stockmq.rpc import RPCTimeoutError


def main():
    parser = argparse.ArgumentParser(description='StockMQ REPL')
    parser.add_argument("uri", type=str, help="Connection URI (example: tcp://127.0.0.1:8004)")
    args = parser.parse_args()
    
    with RPCClient(uri=args.uri) as rpc:
        print("Quik version:", rpc.call("getInfoParam", "VERSION"))
        print("Type exit() to terminate the session")
        while True:
            try:
                x = input(">> ")
                print(rpc.call("stockmq_repl", x))
            except RPCRuntimeError as err:
                print(f"Runtime error: {err}")
            except RPCTimeoutError as err:
                print(f"Timeout error: {err}")

            if x == "exit()":
                break


if __name__ == "__main__":
    main()
