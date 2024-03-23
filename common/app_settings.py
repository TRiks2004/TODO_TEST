from .settings import env, BaseSettings

class SettingsAPI(BaseSettings):
    debug: bool = env.bool('DEBUG_FASTAPI', default=False)
    docs_url: str = env.str('DOCS_URL', default='/docs')
    title: str = env.str('TITLE', default='API(FastAPI)')
    
settings_api = SettingsAPI()





