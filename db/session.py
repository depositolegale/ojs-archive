from connection import engine
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()