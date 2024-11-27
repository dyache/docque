from fastapi import FastAPI
from passlib.context import CryptContext
from sqlalchemy import create_engine

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


engine = create_engine("url", echo = True)
conn = engine.connect()


# TODO: close conn and engine
app = FastAPI()


