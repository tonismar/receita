from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    url_cpf: str
    url_cnpj: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'