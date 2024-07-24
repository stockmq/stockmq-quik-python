from typing import Any
from typing import Mapping

from stockmq.rpc import RPCClient
from stockmq.data import DataSource
from stockmq.data import Timeframe
from stockmq.tx import QuikTx


class QuikTable:
    def __init__(self, rpc: RPCClient, name: str) -> None:
        self.rpc = rpc
        self.name = name

    def __len__(self) -> int:
        return int(self.call("getNumberOf", self.name))

    def __getitem__(self, index) -> Any:
        r = self.call("stockmq_get_item", self.name, index)
        if r is None:
            raise IndexError
        return r


class Quik(RPCClient):
    @property
    def version(self) -> Any:
        return self.call("getInfoParam", "VERSION")

    @property
    def tradedate(self) -> Any:
        return self.call("getInfoParam", "TRADEDATE")

    @property
    def servertime(self) -> Any:
        return self.call("getInfoParam", "SERVERTIME")

    @property
    def lastrecordtime(self) -> Any:
        return self.call("getInfoParam", "LASTRECORDTIME")

    @property
    def numrecords(self) -> Any:
        return self.call("getInfoParam", "NUMRECORDS")

    @property
    def lastrecord(self) -> Any:
        return self.call("getInfoParam", "LASTRECORD")

    @property
    def laterecord(self) -> Any:
        return self.call("getInfoParam", "LATERECORD")

    @property
    def connection(self) -> Any:
        return self.call("getInfoParam", "CONNECTION")

    @property
    def ipaddress(self) -> Any:
        return self.call("getInfoParam", "IPADDRESS")

    @property
    def ipport(self) -> Any:
        return self.call("getInfoParam", "IPPORT")

    @property
    def ipcomment(self) -> Any:
        return self.call("getInfoParam", "IPCOMMENT")

    @property
    def server(self) -> Any:
        return self.call("getInfoParam", "SERVER")

    @property
    def sessionid(self) -> Any:
        return self.call("getInfoParam", "SESSIONID")

    @property
    def user(self) -> Any:
        return self.call("getInfoParam", "USER")

    @property
    def userid(self) -> Any:
        return self.call("getInfoParam", "USERID")

    @property
    def org(self) -> Any:
        return self.call("getInfoParam", "ORG")

    @property
    def localtime(self) -> Any:
        return self.call("getInfoParam", "LOCALTIME")

    @property
    def connectiontime(self) -> Any:
        return self.call("getInfoParam", "CONNECTIONTIME")

    @property
    def messagessent(self) -> Any:
        return self.call("getInfoParam", "MESSAGESSENT")

    @property
    def allsent(self) -> Any:
        return self.call("getInfoParam", "ALLSENT")

    @property
    def bytessent(self) -> Any:
        return self.call("getInfoParam", "BYTESSENT")

    @property
    def bytespersecsent(self) -> Any:
        return self.call("getInfoParam", "BYTESPERSECSENT")

    @property
    def messagesrecv(self) -> Any:
        return self.call("getInfoParam", "MESSAGESRECV")

    @property
    def bytesrecv(self) -> Any:
        return self.call("getInfoParam", "BYTESRECV")

    @property
    def allrecv(self) -> Any:
        return self.call("getInfoParam", "ALLRECV")

    @property
    def bytespersecrecv(self) -> Any:
        return self.call("getInfoParam", "BYTESPERSECRECV")

    @property
    def avgsent(self) -> Any:
        return self.call("getInfoParam", "AVGSENT")

    @property
    def avgrecv(self) -> Any:
        return self.call("getInfoParam", "AVGRECV")

    @property
    def lastpingtime(self) -> Any:
        return self.call("getInfoParam", "LASTPINGTIME")

    @property
    def lastpingduration(self) -> Any:
        return self.call("getInfoParam", "LASTPINGDURATION")

    @property
    def avgpingduration(self) -> Any:
        return self.call("getInfoParam", "AVGPINGDURATION")

    @property
    def maxpingtime(self) -> Any:
        return self.call("getInfoParam", "MAXPINGTIME")

    @property
    def maxpingduration(self) -> Any:
        return self.call("getInfoParam", "MAXPINGDURATION")
    
    @property
    def firms(self) -> QuikTable:
        return QuikTable(self, "firms")

    @property
    def classes(self) -> QuikTable:
        return QuikTable(self, "classes")

    @property
    def securities(self) -> QuikTable:
        return QuikTable(self, "securities")

    @property
    def trade_accounts(self) -> QuikTable:
        return QuikTable(self, "trade_accounts")

    @property
    def client_codes(self) -> QuikTable:
        return QuikTable(self, "client_codes")

    @property
    def all_trades(self) -> QuikTable:
        return QuikTable(self, "all_trades")

    @property
    def account_positions(self) -> QuikTable:
        return QuikTable(self, "account_positions")

    @property
    def orders(self) -> QuikTable:
        return QuikTable(self, "orders")

    @property
    def futures_client_holding(self) -> QuikTable:
        return QuikTable(self, "futures_client_holding")

    @property
    def futures_client_limits(self) -> QuikTable:
        return QuikTable(self, "futures_client_limits")

    @property
    def money_limits(self) -> QuikTable:
        return QuikTable(self, "money_limits")

    @property
    def depo_limits(self) -> QuikTable:
        return QuikTable(self, "depo_limits")

    @property
    def trades(self) -> QuikTable:
        return QuikTable(self, "trades")

    @property
    def stop_orders(self) -> QuikTable:
        return QuikTable(self, "stop_orders")

    @property
    def neg_deals(self) -> QuikTable:
        return QuikTable(self, "neg_deals")

    @property
    def neg_trades(self) -> QuikTable:
        return QuikTable(self, "neg_trades")

    @property
    def neg_deal_reports(self) -> QuikTable:
        return QuikTable(self, "neg_deal_reports")

    @property
    def firm_holding(self) -> QuikTable:
        return QuikTable(self, "firm_holding")

    @property
    def account_balance(self) -> QuikTable:
        return QuikTable(self, "account_balance")

    @property
    def ccp_holdings(self) -> QuikTable:
        return QuikTable(self, "ccp_holdings")

    @property
    def rm_holdings(self) -> QuikTable:
        return QuikTable(self, "rm_holdings")

    @property
    def script_path(self) -> str:
        return self.call("getScriptPath")

    @property
    def working_folder(self) -> str:
        return self.call("getWorkingFolder")

    @property
    def is_connected(self) -> bool:
        return self.call("isConnected") > 0

    @property
    def tx(self) -> QuikTx:
        return QuikTx(self)

    def message(self, message, icon_type=1) -> None:
        self.call("message", message, icon_type)

    def debug(self, message) -> None:
        self.call("PrintDbgStr", message)

    def test(self, payload) -> Any:
        return self.call("stockmq_test", payload)

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
    
    def param(self, class_name: str, sec_name: str, name: str) -> Any:
        return self.call("getParamEx2", class_name, sec_name, name)
    
    def send_transaction(self, transaction: Mapping[str, Any]) -> Any:
        return self.call("sendTransaction", transaction)
    
    def ds(self, board: str, ticker: str, timeframe: Timeframe, timeout: float = 0.05) -> DataSource:
        return DataSource(self, board, ticker, timeframe, timeout)
