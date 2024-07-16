import time
import asyncio
import logging

from enum import Enum
from pydantic import BaseModel
from stockmq.rpc import RPCClient


class TxTimeoutError(Exception):
    pass


class TxRejectedError(Exception):
    pass



class Action(str, Enum):
    NEW_ORDER = "NEW_ORDER"
    NEW_STOP_ORDER = "NEW_STOP_ORDER"
    KILL_ORDER = "KILL_ORDER"
    KILL_STOP_ORDER = "KILL_STOP_ORDER"


class OrderType(str, Enum):
    LIMIT = 'L'
    MARKET = 'M'


class TimeInForce(str, Enum):
    FOK = "FILL_OR_KILL"
    IOC = "KILL_BALANCE"
    DAY = "PUT_IN_QUEUE"


class Side(str, Enum):
    BUY = 'B'
    SELL = 'S'


class TransactionState(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"


class Transaction(BaseModel):
    id: int
    action: Action
    board: str
    order_id: int
    created_ts: float
    updated_ts: float
    state: TransactionState
    message: str


class Order(BaseModel):
    id: int
    board: str


class QuikTx:
    TX_SLEEP_TIMEOUT = 0.01

    def __init__(self, rpc: RPCClient):
        self.rpc = rpc
        self.logger = logging.getLogger(__name__)

    async def wait_tx(self, tx: Transaction, timeout=1.0) -> Transaction:
        t0 = time.time()
        while True:
            if time.time() - t0 >= timeout:
                raise TxTimeoutError()
            elif tx.state == TransactionState.EXECUTED:
                return tx
            elif tx.state == TransactionState.REJECTED:
                self.logger.debug(f"{__name__}: {tx}")
                raise TxRejectedError(tx.message)
            elif tx.state == TransactionState.ACCEPTED:
                await asyncio.sleep(self.TX_SLEEP_TIMEOUT)
                tx = self.update_transaction(tx)
                self.logger.debug(f"{__name__}: {tx}")

    def create_order_tx(self, account: str, client: str, board: str, ticker: str, tif: TimeInForce, side: Side, price: float, quantity: int) -> Transaction:
        return Transaction(**self.rpc.call("stockmq_create_tx", {
            'ACTION': "NEW_ORDER",
            'ACCOUNT': account,
            'CLIENT_CODE': client,
            'CLASSCODE': board,
            'SECCODE': ticker,
            'TYPE':"L",
            'EXECUTION_CONDITION': tif.value,
            'OPERATION': side.value,
            'PRICE': price,
            'QUANTITY': quantity,
        }))

    def create_stop_order_tx(self, account: str, client: str, board: str, ticker: str, tif: TimeInForce, side: Side, price: float, stop_price: float, quantity: int) -> Transaction:
        return Transaction(**self.rpc.call("stockmq_create_tx", {
            'ACTION': "NEW_STOP_ORDER",
            'ACCOUNT': account,
            'CLIENT_CODE': client,
            'CLASSCODE': board,
            'SECCODE': ticker,
            'TYPE': "L",
            'STOP_ORDER_KIND': "SIMPLE_STOP_ORDER",
            'EXECUTION_CONDITION': tif.value,
            'OPERATION': side.value,
            'PRICE': price,
            'STOPPRICE': stop_price,
            'QUANTITY': quantity,
        }))

    def cancel_order_tx(self, account: str, client: str, board: str, ticker: str, order_id: int) -> Transaction:
        return Transaction(**self.rpc.call("stockmq_create_tx", {
            'ACTION': "KILL_ORDER",
            'ACCOUNT': account,
            'CLIENT_CODE': client,
            'CLASSCODE': board,
            'SECCODE': ticker,
            'ORDER_KEY': order_id,
        }))

    def cancel_stop_order_tx(self, account: str, client: str, board: str, ticker: str, order_id: int) -> Transaction:
        return Transaction(**self.rpc.call("stockmq_create_tx", {
            'ACTION': "KILL_STOP_ORDER",
            'ACCOUNT': account,
            'CLIENT_CODE': client,
            'CLASSCODE': board,
            'SECCODE': ticker,
            'STOP_ORDER_KEY': order_id,
        }))

    def update_transaction(self, tx: Transaction) -> Transaction:
        return Transaction(**self.rpc.call("stockmq_update_tx", tx.dict()))

    async def create_order(self, account: str, client: str, board: str, ticker: str, tif: TimeInForce, side: Side, price: float, quantity: int, timeout: float = 1.0) -> Transaction:
        return await self.wait_tx(self.create_order_tx(account, client, board, ticker, tif, side, price, quantity), timeout)

    async def create_stop_order(self, account: str, client: str, board: str, ticker: str, tif: TimeInForce, side: Side, price: float, stop_price: float, quantity: int, timeout: float = 1.0) -> Transaction:
        return await self.wait_tx(self.create_stop_order_tx(account, client, board, ticker, tif, side, price, stop_price, quantity), timeout)

    async def cancel_order(self, account: str, client: str, board: str, ticker: str, order_id: int, timeout: float = 1.0) -> Transaction:
        return await self.wait_tx(self.cancel_order_tx(account, client, board, ticker, order_id), timeout)

    async def cancel_stop_order(self, account: str, client: str, board: str, ticker: str, order_id: int, timeout: float = 1.0) -> Transaction:
        return await self.wait_tx(self.cancel_stop_order_tx(account, client, board, ticker, order_id), timeout)