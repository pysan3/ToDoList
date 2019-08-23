from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__version__ = "0.1.0"

engine = create_engine('sqlite:///apps/database.sqlite3', echo=False)
Base = declarative_base()

Session = sessionmaker(bind=engine)

class Users(Base):
	__tablename__ = 'users'
	id = Column('id', Integer, primary_key=True)
	user_name = Column('user_name', String)
	user_password = Column('user_password', String)
	created_at = Column('created_at', String)

	def __repr__(self):
		return '<Users(id=%s, user_name=%s, user_password=%s, created_at=%s, )>' \
			% (self.id, self.user_name, self.user_password, self.created_at)

class TokenTable(Base):
	__tablename__ = 'tokentable'
	id = Column('id', Integer, primary_key=True)
	token = Column('token', String)
	user_id = Column('user_id', Integer)

	def ___repr__(self):
		return '<TokenTable(id=%s, token=%s, user_id=%s, )>' \
			% (self.id, self.token, self.user_id)