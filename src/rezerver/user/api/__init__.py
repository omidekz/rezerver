from libs import APIRouter
from .user import router as user_crud_router
from .cart import router as cart_crud_router
from .cart_item import router as cart_item_crud_router

routes = APIRouter(prefix='/user')
routes.include_router(user_crud_router)
routes.include_router(cart_crud_router)
routes.include_router(cart_item_crud_router)
