from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from api.routers.auth import auth_router

app = FastAPI()

app.include_router(auth_router)

app.add_middleware(CORSMiddleware,
                   allow_origins=settings.allow_origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])
