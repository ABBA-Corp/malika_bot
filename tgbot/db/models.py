import datetime

from sqlalchemy import Column, VARCHAR, INTEGER, DateTime, BigInteger, sql

from tgbot.db.database import db


class Admin(db.Model):
    __tablename__ = 'admins'
    query: sql.Select

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger(), unique=True)
    name = Column(VARCHAR(50))
    date = Column(DateTime, default=datetime.datetime.utcnow())


class User(db.Model):
    __tablename__ = 'users'
    query: sql.Select

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger(), unique=True)
    name = Column(VARCHAR(200))
    date = Column(DateTime, default=datetime.datetime.utcnow())


class Phone(db.Model):
    __tablename__ = 'phones'
    query: sql.Select

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    model = Column(VARCHAR(200))
    name = Column(VARCHAR(200))
    color = Column(VARCHAR(200))
    month_3 = Column(VARCHAR(200))
    month_4 = Column(VARCHAR(200))
    month_6 = Column(VARCHAR(200))
    month_8 = Column(VARCHAR(200))
    month_12 = Column(VARCHAR(200))
    minimum = Column(VARCHAR(200))
    date = Column(DateTime, default=datetime.datetime.utcnow())
