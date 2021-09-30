from sqlalchemy import create_engine
from api.models.file import Base
from settings import settings


engine = create_engine(settings.db_url, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    reset_database()
