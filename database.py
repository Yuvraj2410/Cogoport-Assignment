from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
from local_settings import DATABASE_URL

Base = declarative_base()


# def get_engine(user, password, host, port, db):
#     url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
#     if not database_exists(url):
#         create_database(url)
#     engine = create_engine(url, pool_size=50, echo=False)
#     return engine
def get_engine():
    engine = create_engine(DATABASE_URL)
    return engine


# engine = create_engine("postgresql://postgres:Galaxy-M31@localhost:5432/CogoportDB")
engine = get_engine()
SessionLocal = sessionmaker(bind=engine)
# engine = get_engine(
#     settings["pguser"],
#     settings["pgpasswd"],
#     settings["pghost"],
#     settings["pgport"],
#     settings["pgdb"],
# )


# def get_engine_from_settings():
#     keys = ["pguser", "pgpasswd", "pghost", "pgport", "pgdb"]
#     if not all(key in keys for key in settings.keys()):
#         raise Exception("Bad config file")

#     return get_engine(
#         settings["pguser"],
#         settings["pgpasswd"],
#         settings["pghost"],
#         settings["pgport"],
#         settings["pgdb"],
#     )


# print(engine.url)


# def get_session():
#     engine = get_engine()
#     # engine = get_engine_from_settings()
#     session = sessionmaker(bind=engine)()
#     return session


# session = get_session()
# print(session)
