import os
from glob import glob
from datetime import datetime

import apps.app as backapp
from apps.database import Base, engine, Session, Users

def create_new_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def init_db():
    backapp.signup({
        'user_name': 'master',
        'user_password': 'password'
    })

if __name__ == '__main__':
    create_new_database()
    init_db()