import datetime

from sqlalchemy import Column, VARCHAR, INTEGER, BOOLEAN, DateTime, BigInteger, sql

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


class Order(db.Model):
    __tablename__ = 'orders'
    query: sql.Select

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(500))
    number = Column(VARCHAR(500))
    passport = Column(VARCHAR(500))
    selfie = Column(VARCHAR(500))
    card = Column(VARCHAR(500))
    time = Column(VARCHAR(500))
    model = Column(VARCHAR(500))
    phone = Column(VARCHAR(500))
    color = Column(VARCHAR(500))
    type = Column(VARCHAR(500))
    status = Column(BOOLEAN())
    date = Column(DateTime, default=datetime.datetime.utcnow())