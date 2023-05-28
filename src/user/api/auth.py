from fdd import APIRouter, service
from pydantic import create_model
from .. import models
import jwt
from datetime import datetime as dt
from setting.env import envs

router = APIRouter(prefix="/auth", tags=["Auth"])
LoginSchema = service.model2schema(
    "LoginSchema",
    models.User,
    _include_={"username"},
    password=(models.user.MD5Str, ...),
)
LoginResponse = create_model("LoginResponse", token=(str, ...), type=(str, ...))
UserRegisterSchema = service.CreateService.model2schema(
    "UserRegisterSchema",
    models.User,
)


@router.post("", response_model=service.create.CreateServiceResponse)
class register_user(service.CreateService):
    repo = models.User
    data: UserRegisterSchema


@router.post("/login", response_model=LoginResponse)
class Login(service.ReadService):
    repo = models.User
    data: LoginSchema

    def _input_phase(self):
        return self.data.dict()

    @classmethod
    def _post_phase(cls, user: models.User):
        return {
            "type": "Bearer ",
            "token": jwt.encode(
                {"pk": user.pk, "at": dt.utcnow().timestamp()},
                envs.secret,
            ),
        }
