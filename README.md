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

Output:

```
(.venv) alex@arm64 stockmq-quik-python % python main.py
Quik version:    11.2.0.16
Quik connection: Информационно-торговая система QUIK "Банк ВТБ (ПАО)"
Is Connected:    True
Last price:      295.990000
                                O       H       L       C      V
T                                                               
2024-07-09 14:07:00+03:00  323.64  323.74  323.63  323.70   2579
2024-07-09 14:08:00+03:00  323.70  323.77  323.65  323.67   6992
2024-07-09 14:09:00+03:00  323.67  323.67  323.66  323.67   1385
2024-07-09 14:10:00+03:00  323.66  323.67  323.61  323.62  11765
2024-07-09 14:11:00+03:00  323.61  323.64  323.61  323.64   1945
...                           ...     ...     ...     ...    ...
2024-07-24 19:51:00+03:00  295.81  295.88  295.80  295.85     36
2024-07-24 19:52:00+03:00  295.85  295.98  295.85  295.91   1293
2024-07-24 19:53:00+03:00  295.91  295.91  295.84  295.90    181
2024-07-24 19:54:00+03:00  295.90  295.98  295.90  295.98    645
2024-07-24 19:55:00+03:00  295.98  295.99  295.93  295.99    760

[6578 rows x 5 columns]
...
```