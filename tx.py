#!/usr/bin/env python3
import asyncio
import time

from stockmq.api import Quik, TimeInForce, Side, QuikTable

api = Quik("tcp://10.211.55.3:8004")

account = "ACCOUNT"
client = "CLIENT"
board = "TQBR"
ticker = "SBER"

async def main():
    with Quik("tcp://10.211.55.3:8004") as api:
        print(f"Quik version: {api.info.VERSION}")
        print(f"Is Connected: {api.is_connected}")

        for i in api.client_codes:
            print(i)

        t0 = time.time()

        # Create transaction to BUY and wait for completion
        tx = await api.create_order(account, client, board, ticker, TimeInForce.DAY, Side.BUY, 265, 1)
        print(tx)
        print(tx.updated_ts - tx.created_ts)

        # Create transaction to cancel the order
        tx = await api.cancel_order(account, client, board, ticker, tx.order_id, timeout=4.0)
        print(tx)
        print(tx.updated_ts - tx.created_ts)

        print(f"Time to create and cancel: {time.time()-t0}")



if __name__ == '__main__':
    asyncio.run(main())