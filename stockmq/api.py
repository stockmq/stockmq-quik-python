from typing import Any

from stockmq.info import QuikInfo
from stockmq.lua import QuikLua
from stockmq.tx import QuikTx
from stockmq.rpc import RPCClient
from stockmq.table import QuikTable





    

class Quik(RPCClient):
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

    @property
    def tx(self) -> QuikTx:
        """Returns Transaction manager"""
        return QuikTx(self)