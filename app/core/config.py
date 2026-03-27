from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    ROLE_ADMIN = 'admin'
    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
settings = Settings()