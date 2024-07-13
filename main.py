#!/usr/bin/env python3
import asyncio
import msgpack
import zmq

from stockmq.rpc import RPCClient
from stockmq.api import Quik
from stockmq.data import DataSource, Timeframe

async def main():
    # Print version and connection information
    with Quik("tcp://10.211.55.3:8004") as api:
        print(f"Quik version: {api.info.version}")
        print(f"Is Connected: {api.is_connected}")

    # Print OLHCV
    with RPCClient("tcp://10.211.55.3:8004") as rpc:
        # Receive a pandas dataframe
        with DataSource(rpc, "SBER", "TQBR", "SBER", Timeframe.M1) as ds:
            print(ds.df())


if __name__ == '__main__':
    asyncio.run(main())