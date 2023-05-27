from fastapi import FastAPI
from fastapi.middleware import cors
from rezerver.user.api import routes as user_router
from rezerver.provider.api import routes as provider_router
from setting.db import DB

app = FastAPI()
app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.on_event("startup")(DB.db_init)
app.on_event("shutdown")(DB.db_shutdown)
app.include_router(user_router, prefix="/api_v1")
app.include_router(provider_router, prefix="/api_v1")
