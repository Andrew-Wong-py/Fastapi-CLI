from typing import Literal, List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    应用配置类
    - 默认值为开发环境配置
    - 生产环境通过 CI/CD 注入环境变量覆盖
    """

    # 环境标识
    ENV: Literal["dev", "prod"] = "dev"

    # 应用信息
    VERSION: str = "0.1.0"

    # 服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 5683

    # 数据库配置
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:SZtu@143237@localhost:5432/earth_diary"
    )

    # CORS 配置
    ORIGINS: List[str] = ["*"]
    METHODS: List[str] = ["*"]
    HEADERS: List[str] = ["*"]

    # Redis 配置（按需启用）
    # REDIS_HOST: str = "localhost"
    # REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(
        env_file=".env",  # 从 .env 文件读取
        env_file_encoding="utf-8",
        case_sensitive=True,  # 环境变量区分大小写
        extra="ignore",  # 忽略额外的环境变量
    )


settings = Settings()
