from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #database
    DATABASE_URL: str 

    #JWT 
    SECRET_KEY: str
    ALGORITHM: str = "HS256" # hmac - imzalama, s256 ise hash fonk. 
                             #jwtyi imzalamak için ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS:  int = 7

    #App 
    APP_NAME: str = "Auth Service" #main.pydaki title, burada logalrda kayıt olması için farklı, amaç farklı.

    DEBUG: bool = False #hata mesajalrının ne kadar detaylı oalcağı, true devleopemtna. bu poroducito
    
    class Config:
        env_file = ".env"

settings = Settings()

