from libs import APIRouter
from .shop import router as shop_router
from .service import router as service_router

routes = APIRouter(prefix="/provider")
routes.include_router(shop_router)
routes.include_router(service_router)
