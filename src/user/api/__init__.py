from fdd import APIRouter
from .profile import router as profile_router
from .auth import router as auth_router

router = APIRouter(prefix="/user")
router.include_router(auth_router)
router.include_router(profile_router)
