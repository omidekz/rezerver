from libs.model.base_model import BaseModel, fields
import typing as t
from hashlib import md5
from setting import envs
from pydantic import constr


class MD5Str(constr(min_length=4, regex=r"[A-Za-z0-9]{4,16}")):
    def hash(self):
        return md5((envs.secret + self).encode()).hexdigest()


class User(BaseModel):
    full_name = fields.CharField(max_length=40)
    username = fields.CharField(max_length=11, unique=True)
    password = fields.CharField(max_length=36)
    nationasl_code = fields.CharField(max_length=10, null=True)
