# Rezerver

## Core

```py
# before :

@router.get(...)
async def api_name(repository_method_params: Schema):
  ... # logic


# after :

@router.post(...)
class api_name(Service):
  # schema
  async def run(self):
    # logic
```

### Core in depth and philosophy

by this structure we can use oop to facilate development and full feature of pydantic validations

- in following example we use `CreateService` to facilate creating simple and complex repository instance and returning create response

```py
from libs import APIRouter
from libs.service import CreateService, CreateServiceResponse
from .. import models


@router.post('', response_model=CreateServiceResponse)
class create_user(CreateService):
  repo = models.User
  data: CreateService.model2schema('CreateUserSchema', models.User)

from fastapi import Depends
from . import middlewares

@router.post('/shop', response_model=CreateServiceResponse)
class create_shop(CreateService):
  repo = models.Shop
  data: CreateService.model2schema('CreateShopSchema', models.Shop)
  user_id: int = Depends(middlewares.jwt2uid)
```
