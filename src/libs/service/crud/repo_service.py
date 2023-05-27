import typing as t
from tortoise.queryset import QuerySet, QuerySetSingle
from tortoise.exceptions import IntegrityError
from libs.model import Model
from ..base import Service
from ..utils import model2schema
import abc
from fastapi import HTTPException, status

ModelClass = t.Type[Model]


class RepoService(Service, abc.ABC):
    repo: t.ClassVar[t.Type[Model]] = None

    @classmethod
    @abc.abstractmethod
    def _method_phase(
        cls,
    ) -> t.Callable[..., t.Union[QuerySet[Model], QuerySetSingle[Model], t.Coroutine]]:
        ...

    def _input_phase(self, **kw) -> dict:
        return self.dict(**kw)

    def _filter_phase(self, q: t.Union[QuerySet, t.Coroutine]):
        return q

    def _post_phase(self, result: any):
        return result

    @classmethod
    def model2schema(cls, name: str, model: ModelClass, **kw):
        return model2schema(name, model, **kw)

    async def run(self):
        repo_method = self._method_phase()
        try:
            result = await self._filter_phase(repo_method(**self._input_phase()))
            return self._post_phase(result)
        except IntegrityError as ie:
            ie_msg = str(ie)
            if ie_msg.lower().startswith("unique"):
                sc, det = status.HTTP_409_CONFLICT, {"field": ie_msg.split(" ")[-1]}
            else:
                sc, det = status.HTTP_500_INTERNAL_SERVER_ERROR, {"msg": str(ie)}
            raise HTTPException(status_code=sc, detail=det)
