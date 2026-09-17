import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
Base = declarative_base()
load_dotenv()
DB_USER = quote_plus(os.getenv("DB_USER"))
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:"
    f"{DB_PASSWORD}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)