import inspect
import makefun
from functools import wraps
from typing import Any, Callable, Type
from fastapi import APIRouter as _APIRouter
from .service.base import Service


class APIRouter(_APIRouter):
    @staticmethod
    def make_callback(endpoint: Type[Service]):
        @wraps(endpoint)
        async def callback(*args, **kwargs):
            return await endpoint(*args, **kwargs).run()

        return callback

    def gen_sign(endpoint: Type[Service]):
        return inspect.signature(endpoint)

    @classmethod
    def service2endpoint(cls, endpoint: Type[Service]):
        return makefun.create_function(
            func_signature=cls.gen_sign(endpoint),
            func_impl=cls.make_callback(endpoint),
            func_name=endpoint.__name__,
        )

    def add_api_route(self, path: str, endpoint: Callable[..., Any], **kw):
        if isinstance(endpoint, type) and issubclass(endpoint, Service):
            endpoint = self.service2endpoint(endpoint)
        return super().add_api_route(path, endpoint, **kw)
