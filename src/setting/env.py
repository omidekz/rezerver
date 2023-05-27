from pydantic import BaseSettings
import hashids


class Envs(BaseSettings):
    class Config:
        env_file = ".env"

    secret: str = "gzUZa"
    admin_ups: str = ""
    db_url: str = "sqlite://db.sqlite3"


envs = Envs()
hashids = hashids.Hashids(envs.secret, min_length=3)
