from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class Product(Base):

    __tablename__ = "products"


    id = Column(
        Integer,
        primary_key=True
    )

    store = Column(
        String
    )

    product = Column(
        String
    )

    price = Column(
        String
    )