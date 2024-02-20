from typing import Any

from stockmq.rpc import RPCClient


class QuikInfo:
    def __init__(self, rpc: RPCClient):
        self.rpc = rpc

    @property
    def VERSION(self) -> Any:
        return self.rpc.call("getInfoParam", "VERSION")

    @property
    def TRADEDATE(self) -> Any:
        return self.rpc.call("getInfoParam", "TRADEDATE")

    @property
    def SERVERTIME(self) -> Any:
        return self.rpc.call("getInfoParam", "SERVERTIME")

    @property
    def LASTRECORDTIME(self) -> Any:
        return self.rpc.call("getInfoParam", "LASTRECORDTIME")

    @property
    def NUMRECORDS(self) -> Any:
        return self.rpc.call("getInfoParam", "NUMRECORDS")

    @property
    def LASTRECORD(self) -> Any:
        return self.rpc.call("getInfoParam", "LASTRECORD")

    @property
    def LATERECORD(self) -> Any:
        return self.rpc.call("getInfoParam", "LATERECORD")

    @property
    def CONNECTION(self) -> Any:
        return self.rpc.call("getInfoParam", "CONNECTION")

    @property
    def IPADDRESS(self) -> Any:
        return self.rpc.call("getInfoParam", "IPADDRESS")

    @property
    def IPPORT(self) -> Any:
        return self.rpc.call("getInfoParam", "IPPORT")

    @property
    def IPCOMMENT(self) -> Any:
        return self.rpc.call("getInfoParam", "IPCOMMENT")

    @property
    def SERVER(self) -> Any:
        return self.rpc.call("getInfoParam", "SERVER")

    @property
    def SESSIONID(self) -> Any:
        return self.rpc.call("getInfoParam", "SESSIONID")

    @property
    def USER(self) -> Any:
        return self.rpc.call("getInfoParam", "USER")

    @property
    def USERID(self) -> Any:
        return self.rpc.call("getInfoParam", "USERID")

    @property
    def ORG(self) -> Any:
        return self.rpc.call("getInfoParam", "ORG")

    @property
    def LOCALTIME(self) -> Any:
        return self.rpc.call("getInfoParam", "LOCALTIME")

    @property
    def CONNECTIONTIME(self) -> Any:
        return self.rpc.call("getInfoParam", "CONNECTIONTIME")

    @property
    def MESSAGESSENT(self) -> Any:
        return self.rpc.call("getInfoParam", "MESSAGESSENT")

    @property
    def ALLSENT(self) -> Any:
        return self.rpc.call("getInfoParam", "ALLSENT")

    @property
    def BYTESSENT(self) -> Any:
        return self.rpc.call("getInfoParam", "BYTESSENT")

    @property
    def BYTESPERSECSENT(self) -> Any:
        return self.rpc.call("getInfoParam", "BYTESPERSECSENT")

    @property
    def MESSAGESRECV(self) -> Any:
        return self.rpc.call("getInfoParam", "MESSAGESRECV")

    @property
    def BYTESRECV(self) -> Any:
        return self.rpc.call("getInfoParam", "BYTESRECV")

    @property
    def ALLRECV(self) -> Any:
        return self.rpc.call("getInfoParam", "ALLRECV")

    @property
    def BYTESPERSECRECV(self) -> Any:
        return self.rpc.call("getInfoParam", "BYTESPERSECRECV")

    @property
    def AVGSENT(self) -> Any:
        return self.rpc.call("getInfoParam", "AVGSENT")

    @property
    def AVGRECV(self) -> Any:
        return self.rpc.call("getInfoParam", "AVGRECV")

    @property
    def LASTPINGTIME(self) -> Any:
        return self.rpc.call("getInfoParam", "LASTPINGTIME")

    @property
    def LASTPINGDURATION(self) -> Any:
        return self.rpc.call("getInfoParam", "LASTPINGDURATION")

    @property
    def AVGPINGDURATION(self) -> Any:
        return self.rpc.call("getInfoParam", "AVGPINGDURATION")

    @property
    def MAXPINGTIME(self) -> Any:
        return self.rpc.call("getInfoParam", "MAXPINGTIME")

    @property
    def MAXPINGDURATION(self) -> Any:
        return self.rpc.call("getInfoParam", "MAXPINGDURATION")