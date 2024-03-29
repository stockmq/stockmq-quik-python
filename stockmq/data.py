import time
import enum

from stockmq.rpc import RPCClient
import pandas as pd

from typing import Any


class Timeframe(str, enum.Enum):
    TICK = "TICK"
    M1 = "M1"
    M2 = "M2"
    M3 = "M3"
    M4 = "M4"
    M5 = "M5"
    M6 = "M6"
    M10 = "M10"
    M15 = "M15"
    M20 = "M20"
    M30 = "M30"
    H1 = "H1"
    H2 = "H2"
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"
    MN1 = "MN1"


class DataSource:
    def __init__(self, rpc: RPCClient, name: str, board: str, ticker: str, timeframe: Timeframe, stream: bool = False,
                 timeout: float = 0.05):
        self.rpc = rpc
        self.key = self.rpc.call("stockmq_ds_create", name, board, ticker, timeframe.value, stream)
        self.timeout = timeout

    def __enter__(self):
        while len(self) == 0:
            time.sleep(self.timeout)
        return self

    def __exit__(self, *args: Any, **kwargs: Any):
        self.close()

    def __len__(self):
        return self.rpc.call("stockmq_ds_size", self.key)

    def __getitem__(self, index):
        if r := self.rpc.call("stockmq_ds_peek", self.key, index):
            return r
        else:
            raise IndexError

    def close(self) -> None:
        self.rpc.call("stockmq_ds_delete", self.key)

    def df(self, tz: str = 'Europe/Moscow') -> pd.DataFrame:
        columns = ['T', 'O', 'H', 'L', 'C', 'V']
        if len(self):
            df = pd.DataFrame.from_records(self).reindex(columns=columns).set_index('T')
            df.index = pd.to_datetime(df.index, unit='s', utc=True).tz_convert(tz)
            return df
        else:
            return pd.DataFrame(columns=columns).set_index('T')
