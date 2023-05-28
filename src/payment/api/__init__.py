from fdd.router import APIRouter
from .cart import router as cart_crud_router
from .cart_item import router as item_crud_router

router = APIRouter(prefix="/pay")
router.include_router(cart_crud_router)
router.include_router(item_crud_router)
