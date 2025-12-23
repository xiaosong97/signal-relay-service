from functools import lru_cache
import os
from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

# settings.py 必须位于 app/ 目录下
# BASE_DIR = project root
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


class Settings(BaseSettings):
    """
    APP_ENV 决定运行环境
    - dev: 本地开发(默认)
    - test: 测试(允许内存DB)
    - prod: 生产/Docker/服务器
    """

    APP_ENV: Literal["dev", "test", "prod"] = "dev"
    # 用于 API 鉴权
    API_TOKEN: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def DB_URL(self) -> str:
        """
        根据 APP_ENV 自动推导 DB_URL
        """
        if self.APP_ENV == "test":
            # 只在测试中允许 memory
            return "sqlite:///:memory:"
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if self.APP_ENV == "prod":
            # Docker / 服务器
            return f"sqlite:///{DATA_DIR / 'prod.db'}"
        # 默认 dev
        return f"sqlite:///{DATA_DIR / 'dev.db'}"

# —— Settings 工厂层 —— #

@lru_cache()
def _get_settings_cached(app_env: str) -> Settings:
    """
    每个 APP_ENV 对应一份 Settings
    """
    if app_env == "test":
        # test 环境：明确不加载 .env
        return Settings(_env_file=None)

    # dev / prod：允许 .env
    return Settings()


def clear_settings_cache() -> None:
    """
    仅用于测试：清空 Settings 缓存
    """
    _get_settings_cached.cache_clear()


def get_settings() -> Settings:
    app_env = os.getenv("APP_ENV", "dev")
    return _get_settings_cached(app_env)