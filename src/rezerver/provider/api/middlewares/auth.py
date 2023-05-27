from fastapi import Depends as _Depends
from rezerver.user.api.middlewares import jwt2user_id as _jwt2user_id
from libs.service import RepoService as _RepoService
from fastapi import Path as _Path
from ... import models as _models
import typing as _t


class ShopOwnerAccess(_RepoService):
    user_id: int = _Depends(_jwt2user_id)

    def _input_phase(self) -> dict:
        return {**super()._input_phase(), "shop__user_id": self.user_id}


def provider_username2id_base(
    default: _t.Any = ...,
    *,
    iden_type=None,
    method=_Path,
    **kw,
):
    iden_type_ = iden_type or _t.Union[int, str]

    async def _deco(shop_iden: iden_type_ = method(default, **kw)):
        shop_id = (
            shop_iden
            if isinstance(shop_iden, int)
            else (await _models.Shop.get_or_404(username=shop_iden)).pk
        )
        return shop_id

    return _deco


provider_username2id = provider_username2id_base(
    alias="provider_id", description="enter `provider_id` or it' `username`"
)


async def provider_username2id_if_owner(
    shop_id: int = _Depends(provider_username2id),
    user_id: int = _Depends(_jwt2user_id),
):
    return _models.Shop.get_or_404(pk=shop_id, user_id=user_id)
