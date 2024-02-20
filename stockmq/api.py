import time
import asyncio

from enum import Enum
from pydantic import BaseModel
from typing import Any

from stockmq.ns.info import QuikInfo
from stockmq.ns.lua import QuikLua
from stockmq.rpc import RPCClient
from stockmq.ns.table import QuikTable


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






    

class Quik(RPCClient):
    TX_SLEEP_TIMEOUT = 0.01

    @property
    def lua(self) -> QuikLua:
        return QuikLua(self)

    @property
    def info(self) -> QuikInfo:
        return QuikInfo(self)

    @property
    def script_path(self) -> str:
        return self.call("getScriptPath")

    @property
    def working_folder(self) -> str:
        return self.call("getWorkingFolder")

    @property
    def is_connected(self) -> bool:
        return self.call("isConnected") > 0

    def message(self, message, icon_type=1) -> None:
        self.call("message", message, icon_type)

    def debug(self, message) -> None:
        self.call("PrintDbgStr", message)

    def test(self, payload) -> Any:
        return self.call("stockmq_test", payload)

    @property
    def firms(self) -> Any:
        return QuikTable(self, "firms")

    @property
    def classes(self) -> Any:
        return QuikTable(self, "classes")

    @property
    def securities(self) -> Any:
        return QuikTable(self, "securities")

    @property
    def trade_accounts(self) -> Any:
        return QuikTable(self, "trade_accounts")

    @property
    def client_codes(self) -> Any:
        return QuikTable(self, "client_codes")

    @property
    def all_trades(self) -> Any:
        return QuikTable(self, "all_trades")

    @property
    def account_positions(self) -> Any:
        return QuikTable(self, "account_positions")

    @property
    def orders(self) -> Any:
        return QuikTable(self, "orders")

    @property
    def futures_client_holding(self) -> Any:
        return QuikTable(self, "futures_client_holding")

    @property
    def futures_client_limits(self) -> Any:
        return QuikTable(self, "futures_client_limits")

    @property
    def money_limits(self) -> Any:
        return QuikTable(self, "money_limits")

    @property
    def depo_limits(self) -> Any:
        return QuikTable(self, "depo_limits")

    @property
    def trades(self) -> Any:
        return QuikTable(self, "trades")

    @property
    def stop_orders(self) -> Any:
        return QuikTable(self, "stop_orders")

    @property
    def neg_deals(self) -> Any:
        return QuikTable(self, "neg_deals")

    @property
    def neg_trades(self) -> Any:
        return QuikTable(self, "neg_trades")

    @property
    def neg_deal_reports(self) -> Any:
        return QuikTable(self, "neg_deal_reports")

    @property
    def firm_holding(self) -> Any:
        return QuikTable(self, "firm_holding")

    @property
    def account_balance(self) -> Any:
        return QuikTable(self, "account_balance")

    @property
    def ccp_holdings(self) -> Any:
        return QuikTable(self, "ccp_holdings")

    @property
    def rm_holdings(self) -> Any:
        return QuikTable(self, "rm_holdings")

    def repl(self, s: str) -> Any:
        return self.call("stockmq_repl", s)

    def get_table(self, name: str) -> QuikTable:
        return QuikTable(self, name)

    def get_classes(self) -> Any:
        return filter(len, self.call("getClassesList").split(","))

    def get_class_info(self, class_name) -> Any:
        return self.call("getClassInfo", class_name)

    def get_class_securities(self, class_name) -> Any:
        return filter(len, self.call("getClassSecurities", class_name).split(","))

    def get_security_info(self, class_name, sec_name) -> Any:
        return self.call("getSecurityInfo", class_name, sec_name)

    async def wait_tx(self, tx: Transaction, timeout=1.0) -> Transaction:
        t0 = time.time()
        while True:
            if time.time() - t0 >= timeout:
                raise TxTimeoutError()
            elif tx.state == TransactionState.EXECUTED:
                return tx
            elif tx.state == TransactionState.REJECTED:
                print(tx)
                raise TxRejectedError(tx.message)
            elif tx.state == TransactionState.ACCEPTED:
                await asyncio.sleep(self.TX_SLEEP_TIMEOUT)
                tx = self.update_transaction(tx)
                print(tx)

    def create_order_tx(self, account: str, client: str, board: str, ticker: str, tif: TimeInForce, side: Side, price: float, quantity: int) -> Transaction:
        return Transaction(**self.call("stockmq_create_order", account, client, board, ticker, tif.value, side.value, price, quantity))

    def create_stop_order_tx(self, account: str, client: str, board: str, ticker: str, tif: TimeInForce, side: Side, price: float, stop_price: float, quantity: int) -> Transaction:
        return Transaction(**self.call("stockmq_create_simple_stop_order", account, client, board, ticker, tif.value, side.value, price, stop_price, quantity))

    def cancel_order_tx(self, account: str, client: str, board: str, ticker: str, order_id: int) -> Transaction:
        return Transaction(**self.call("stockmq_cancel_order", account, client, board, ticker, order_id))

    def cancel_stop_order_tx(self, account: str, client: str, board: str, ticker: str, order_id: int) -> Transaction:
        return Transaction(**self.call("stockmq_cancel_stop_order", account, client, board, ticker, order_id))

    def update_transaction(self, tx: Transaction) -> Transaction:
        return Transaction(**self.call("stockmq_update_tx", tx.dict()))

    async def create_order(self, account: str, client: str, board: str, ticker: str, tif: TimeInForce, side: Side, price: float, quantity: int, timeout: float = 1.0) -> Transaction:
        return await self.wait_tx(self.create_order_tx(account, client, board, ticker, tif, side, price, quantity), timeout)

    async def create_stop_order(self, account: str, client: str, board: str, ticker: str, tif: TimeInForce, side: Side, price: float, stop_price: float, quantity: int, timeout: float = 1.0) -> Transaction:
        return await self.wait_tx(self.create_stop_order_tx(account, client, board, ticker, tif, side, price, stop_price, quantity), timeout)

    async def cancel_order(self, account: str, client: str, board: str, ticker: str, order_id: int, timeout: float = 1.0) -> Transaction:
        return await self.wait_tx(self.cancel_order_tx(account, client, board, ticker, order_id), timeout)

    async def cancel_stop_order(self, account: str, client: str, board: str, ticker: str, order_id: int, timeout: float = 1.0) -> Transaction:
        return await self.wait_tx(self.cancel_stop_order_tx(account, client, board, ticker, order_id), timeout)
