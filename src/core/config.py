import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, MySQLDsn

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(dotenv_path=BASE_DIR / ".env")  # for local development


def get_required_env(env_var_name: str) -> str:
    env_var = os.getenv(env_var_name)
    if env_var is None:
        raise RuntimeError(f"The environment variable {env_var_name} is not set")
    return env_var


class DbSettings(BaseModel):
    url: MySQLDsn = MySQLDsn(get_required_env("DB_URL"))
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }


class Settings(BaseModel):
    base_dir: Path = BASE_DIR
    db: DbSettings = DbSettings()


settings = Settings()
