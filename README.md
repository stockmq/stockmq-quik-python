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

uri = "tcp://127.0.0.1:8004"
account = "ACCOUNT"
client = "CLIENT"
board = "TQBR"
ticker = "SBER"


async def main():    
    with Quik(uri) as api:
        # Print version and connection information
        print(f"Quik version:    {api.version}")
        print(f"Quik connection: {api.server}")
        print(f"Is Connected:    {api.is_connected}")
        print(f"Last price:      {api.param(board, ticker, 'LAST')['param_value']}")

        # Print OLHCV as Pandas dataframe
        with api.ds(board, ticker, Timeframe.M1) as ds:
            print(ds.df())

        # Create transaction to BUY and wait for completion
        t0 = time.time()
        tx = await api.tx.create_order(account, client, board, ticker,
                                      TimeInForce.DAY, Side.BUY, 
                                      265.00, 1)
        print(tx)
        print(tx.updated_ts - tx.created_ts)

        # Create transaction to cancel the order
        tx = await api.tx.cancel_order(account, client, board, ticker, 
                                       tx.order_id, timeout=4.0)
        print(tx)
        print(tx.updated_ts - tx.created_ts)

        print(f"Time to create and cancel: {time.time() - t0}")



if __name__ == '__main__':
    asyncio.run(main())
```
