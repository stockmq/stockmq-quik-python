from stockmq.rpc import RPCClient


class Param:
    def __init__(self, rpc: RPCClient, board: str, ticker: str):
        self.rpc = rpc
        self.board = board
        self.ticker = ticker

    def __getitem__(self, index):
        if r := self.rpc.call("getParamEx2", self.board, self.ticker, index):
            return r
        else:
            raise IndexError