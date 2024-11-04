# import os
# from sqlalchemy.orm import declarative_base
# from sqlalchemy import create_engine, URL
#
# Base = declarative_base()
#
#
# def get_engine():
#     return create_engine(
#         URL.create(
#             drivername="postgresql",
#             username=os.environ["POSTGRES_USER"],
#             password=os.environ["POSTGRES_PASSWORD"],
#             host=os.environ["POSTGRES_HOST"],
#             port=int(os.environ["POSTGRES_PORT"]),
#             database=os.environ["POSTGRES_DB"],
#         )
#     )
