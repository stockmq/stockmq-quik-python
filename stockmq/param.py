from typing import Any

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


class QuikInfo:
    def __init__(self, rpc: RPCClient):
        self.rpc = rpc

    @property
    def version(self) -> Any:
        return self.rpc.call("getInfoParam", "VERSION")

    @property
    def tradedate(self) -> Any:
        return self.rpc.call("getInfoParam", "TRADEDATE")

    @property
    def servertime(self) -> Any:
        return self.rpc.call("getInfoParam", "SERVERTIME")

    @property
    def lastrecordtime(self) -> Any:
        return self.rpc.call("getInfoParam", "LASTRECORDTIME")

    @property
    def numrecords(self) -> Any:
        return self.rpc.call("getInfoParam", "NUMRECORDS")

    @property
    def lastrecord(self) -> Any:
        return self.rpc.call("getInfoParam", "LASTRECORD")

    @property
    def laterecord(self) -> Any:
        return self.rpc.call("getInfoParam", "LATERECORD")

    @property
    def connection(self) -> Any:
        return self.rpc.call("getInfoParam", "CONNECTION")

    @property
    def ipaddress(self) -> Any:
        return self.rpc.call("getInfoParam", "IPADDRESS")

    @property
    def ipport(self) -> Any:
        return self.rpc.call("getInfoParam", "IPPORT")

    @property
    def ipcomment(self) -> Any:
        return self.rpc.call("getInfoParam", "IPCOMMENT")

    @property
    def server(self) -> Any:
        return self.rpc.call("getInfoParam", "SERVER")

    @property
    def sessionid(self) -> Any:
        return self.rpc.call("getInfoParam", "SESSIONID")

    @property
    def user(self) -> Any:
        return self.rpc.call("getInfoParam", "USER")

    @property
    def userid(self) -> Any:
        return self.rpc.call("getInfoParam", "USERID")

    @property
    def org(self) -> Any:
        return self.rpc.call("getInfoParam", "ORG")

    @property
    def localtime(self) -> Any:
        return self.rpc.call("getInfoParam", "LOCALTIME")

    @property
    def connectiontime(self) -> Any:
        return self.rpc.call("getInfoParam", "CONNECTIONTIME")

    @property
    def messagessent(self) -> Any:
        return self.rpc.call("getInfoParam", "MESSAGESSENT")

    @property
    def allsent(self) -> Any:
        return self.rpc.call("getInfoParam", "ALLSENT")

    @property
    def bytessent(self) -> Any:
        return self.rpc.call("getInfoParam", "BYTESSENT")

    @property
    def bytespersecsent(self) -> Any:
        return self.rpc.call("getInfoParam", "BYTESPERSECSENT")

    @property
    def messagesrecv(self) -> Any:
        return self.rpc.call("getInfoParam", "MESSAGESRECV")

    @property
    def bytesrecv(self) -> Any:
        return self.rpc.call("getInfoParam", "BYTESRECV")

    @property
    def allrecv(self) -> Any:
        return self.rpc.call("getInfoParam", "ALLRECV")

    @property
    def bytespersecrecv(self) -> Any:
        return self.rpc.call("getInfoParam", "BYTESPERSECRECV")

    @property
    def avgsent(self) -> Any:
        return self.rpc.call("getInfoParam", "AVGSENT")

    @property
    def avgrecv(self) -> Any:
        return self.rpc.call("getInfoParam", "AVGRECV")

    @property
    def lastpingtime(self) -> Any:
        return self.rpc.call("getInfoParam", "LASTPINGTIME")

    @property
    def lastpingduration(self) -> Any:
        return self.rpc.call("getInfoParam", "LASTPINGDURATION")

    @property
    def avgpingduration(self) -> Any:
        return self.rpc.call("getInfoParam", "AVGPINGDURATION")

    @property
    def maxpingtime(self) -> Any:
        return self.rpc.call("getInfoParam", "MAXPINGTIME")

    @property
    def maxpingduration(self) -> Any:
        return self.rpc.call("getInfoParam", "MAXPINGDURATION")