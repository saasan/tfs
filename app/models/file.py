from sqlalchemy import Column, String, BigInteger
from db import Base


class File(Base):
    __tablename__ = 'files'

    id = Column(String(26), primary_key=True, nullable=False)
    upload_epoch_ms = Column(BigInteger, nullable=False)
    name = Column(String(1024), nullable=False)
    size = Column(BigInteger, nullable=False)
    human_readable_size = Column(String(20), nullable=False)
