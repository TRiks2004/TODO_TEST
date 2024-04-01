from .settings import env, BaseSettings


class SettingsRedis(BaseSettings):
    port: str = env.str('INTERNAL_PORT_REDIS', default='6379')
    host: str = env.str('INTERNAL_HOST_POSTGRES', default='localhost')

    @property
    def url(self):
        return f'redis://{self.host}:{self.port}'


settings_redis = SettingsRedis()
