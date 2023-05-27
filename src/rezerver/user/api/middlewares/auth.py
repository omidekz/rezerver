from fastapi import Header as _Header, HTTPException as _HTTPException
from pydantic import constr as _constr
import jwt as _jwt
from setting import envs as _envs


async def jwt2user_id(authorization: str = _Header(...)):
    try:
        user_pk = _jwt.decode(authorization[7:], _envs.secret, ["HS256"])["pk"]
        return user_pk
    except:
        raise _HTTPException(403, detail={"code": 403, "msg": "bad token"})


async def optional_jwt2user_id(
    authorization: _constr(regex=r".+") = _Header(None),
):
    if authorization:
        return jwt2user_id(authorization)
