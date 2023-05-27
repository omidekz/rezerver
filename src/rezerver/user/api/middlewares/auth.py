from fastapi import Header, HTTPException
from pydantic import constr
import jwt
from setting import envs


async def jwt2user_id(authorization: str = Header(...)):
    try:
        user_pk = jwt.decode(authorization[7:], envs.secret, ["HS256"])["pk"]
        return user_pk
    except:
        raise HTTPException(403, detail={"code": 403, "msg": "bad token"})


async def optional_jwt2user_id(
    authorization: constr(regex=r"^Bearer .*") = Header(None),
):
    if authorization:
        return jwt2user_id(authorization)
