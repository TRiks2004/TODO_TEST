from .settings import env, BaseSettings
from sqlalchemy import URL


class SettingsAlembic(BaseSettings):
    db_name: str = env.str("POSTGRES_DB")
    db_host: str = env.str("EXTERNAL_HOST_POSTGRES")
    db_port: int = env.int("EXTERNAL_PORT_POSTGRES")
    db_user: str = env.str("POSTGRES_USER")
    db_password: str = env.str("POSTGRES_PASSWORD")
    db_debug: bool = env.bool("POSTGRES_DEBUG", default=False)

    @property
    def db_url_async(self) -> URL:
        # postgresql+asyncpg://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(EXTERNAL_HOST_POSTGRES):(EXTERNAL_PORT_POSTGRES)/$(POSTGRES_DB)
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings_alembic = SettingsAlembic()
