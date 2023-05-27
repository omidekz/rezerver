from rezerver.user.api.middlewares import jwt2user_id
from ...models import Cart
from fastapi import Depends as _Depends, HTTPException as _HTTPException


async def owner_access2cart(cart_id: int, user_id: int = _Depends(jwt2user_id)):
    if await Cart.get_or_404(pk=cart_id, user_id=user_id):
        return cart_id
    raise _HTTPException(403)
