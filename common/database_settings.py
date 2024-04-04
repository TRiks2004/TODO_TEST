from .settings import env, BaseSettings
from sqlalchemy import URL


class SettingsDatabase(BaseSettings):
    db_name: str = env.str("POSTGRES_DB")
    db_host: str = env.str("EXTERNAL_HOST_POSTGRES")
    db_port: int = env.int("EXTERNAL_PORT_POSTGRES")
    db_user: str = env.str("POSTGRES_USER")
    db_password: str = env.str("POSTGRES_PASSWORD")
    db_debug: bool = env.bool("POSTGRES_DEBUG", default=False)

    @property
    def db_url_async(self) -> URL:

        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )


settings_database = SettingsDatabase()
