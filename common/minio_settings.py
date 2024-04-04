from .settings import env, BaseSettings


class SettingsMinio(BaseSettings):
    port: int = env.str("EXTERNAL_PORT_MINIO", default=9000)
    host: str = env.str("EXTERNAL_HOST_MINIO", default="localhost")

    access_key: str = env.str("MINIO_ACCESS_KEY_API")
    secret_key: str = env.str("MINIO_SECRET_KEY_API")


settings_minio = SettingsMinio()
print(settings_minio)
