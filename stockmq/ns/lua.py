from typing import Any

from stockmq.rpc import RPCClient


class QuikLua:
    def __init__(self, rpc: RPCClient):
        self.rpc = rpc

    def __getattr__(self, item: Any) -> Any:
        def wrapper(*args, **kwargs) -> Any:
            return self.rpc.call(item, *args)
        return wrapper