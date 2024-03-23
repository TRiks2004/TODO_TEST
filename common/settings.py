import environ
import pathlib

from pydantic_settings import BaseSettings


BASE_DIR = pathlib.Path(__file__).parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')










