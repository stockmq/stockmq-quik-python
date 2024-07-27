import zmq
import msgpack

from typing import Any
from typing import Optional
from typing import Self


class RPCRuntimeError(Exception):
    """Runtime Error (error on server)"""
    pass


class RPCTimeoutError(Exception):
    """Timeout Error"""
    pass


class RPCClient:
    """RPC Client"""
    RPC_OK = 'OK'

    def __init__(self, uri: str = 'tcp://127.0.0.1:8004', timeout: int = 100) -> None:
        """Set up the REQ socket and connect"""
        self.timeout = timeout
        self.zmq_ctx = zmq.Context()
        self.zmq_skt = self.zmq_ctx.socket(zmq.REQ)
        self.zmq_skt.setsockopt(zmq.RCVTIMEO, timeout)
        self.zmq_skt.setsockopt(zmq.LINGER, 0)
        self.zmq_skt.connect(uri)

    def __enter__(self) -> Self:
        """Enter the context"""
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Close the connection when leaving the context"""
        self.close()

    def call(self, method: str, *args: Any, timeout: Optional[int] = None) -> Any:
        """Call RPC method"""
        self.zmq_skt.send(msgpack.packb([method, *args]))
        if self.zmq_skt.poll(timeout or self.timeout) == zmq.POLLIN:
            s1, s2 = self.zmq_skt.recv_multipart()
            status = s1.decode()
            result = msgpack.unpackb(s2, strict_map_key=False)

            if status == self.RPC_OK:
                return result
            else:
                raise RPCRuntimeError(result)
        else:
            raise RPCTimeoutError()

    def close(self) -> None:
        """Close the socket and terminate the context"""
        self.zmq_skt.close()
        self.zmq_ctx.term()
