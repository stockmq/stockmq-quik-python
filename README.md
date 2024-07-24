# stockmq-quik-python
Python bindings for StockMQ QUIK

# Example

This code places an order and cancels it immediately.

```python
#!/usr/bin/env python3
import asyncio
import time

from stockmq.api import Quik
from stockmq.tx import TimeInForce, Side

account = "ACCOUNT"
client = "CLIENT"
board = "TQBR"
ticker = "SBER"


async def main():
    # Create transaction to BUY and cancel
    with Quik("tcp://10.211.55.3:8004") as api:
        print(f"Quik version:    {api.version}")
        print(f"Quik connection: {api.server}")
        print(f"Is Connected:    {api.is_connected}")
        print(f"Last:            {api.param('TQBR', 'SBER', 'LAST')['param_value']}"}

        # Create transaction to BUY and wait for completion
        t0 = time.time()
        tx = await api.tx.create_order(account, client, board, ticker, TimeInForce.DAY, Side.BUY, 265, 1)
        print(tx)
        print(tx.updated_ts - tx.created_ts)

        # Create transaction to cancel the order
        tx = await api.tx.cancel_order(account, client, board, ticker, tx.order_id, timeout=4.0)
        print(tx)
        print(tx.updated_ts - tx.created_ts)

        print(f"Time to create and cancel: {time.time() - t0}")

    # Print OLHCV as Pandas dataframe
    with RPCClient("tcp://10.211.55.3:8004") as rpc:
        # Receive a pandas dataframe
        with DataSource(rpc, "TQBR", "SBER", Timeframe.M1) as ds:
            print(ds.df())


if __name__ == '__main__':
    asyncio.run(main())
```
