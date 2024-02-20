from stockmq.rpc import RPCClient


class QuikTable:
    def __init__(self, rpc: RPCClient, name: str):
        self.rpc = rpc
        self.name = name

    def __len__(self):
        return int(self.rpc.call("getNumberOf", self.name))

    def __getitem__(self, index):
        r = self.rpc.call("stockmq_get_item", self.name, index)
        if r is None:
            raise IndexError
        return r
