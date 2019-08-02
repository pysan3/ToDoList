import numpy as np
import hashlib
from datetime import datetime

from apps.database import Session, Users

def login(data):
    session = Session()
    user = session.query(Users).filter_by(user_name=data['user_name']).all()
    session.close()
    user_id = -1
    password = hashlib.sha256(data['user_password'].encode()).hexdigest()
    if len(user) == 1:
        if user[0].user_password == password:
            msg = 'success'
            user_id = user[0].id
        else:
            msg = 'wrong password'
    else:
        msg = 'wrong username'
    return {'isFound': len(user), 'user_id': user_id, 'msg': msg}

def signup(data):
    name = data['user_name']
    user_id = -1
    session = Session()
    user = session.query(Users).filter_by(user_name=name).all()
    if len(user) == 0:
        user_id = session.query(Users).count() + 1
        session.add(Users(
            user_name=name,
            user_password=hashlib.sha256(data['user_password'].encode()).hexdigest(),
            created_at=datetime.now().isoformat(' ', 'seconds')
        ))
        session.commit()
        msg = 'succeeded to create an user account'
    else:
        msg = 'already exists'
    session.close()
    return {'isFound': user_id>=0 + 0, 'user_id': user_id, 'msg': msg}

def logged_in(user_id):
    if user_id < 2:
        return 0
    session = Session()
    result = session.query(Eventlogs).filter_by(user_id=user_id).all()
    event_id_logout = session.query(Eventnames).filter_by(event_name='logout').one().id - 1
    session.close()
    if len(result) == 0 or result[-1].event_id == event_id_logout:
        return 0
    else:
        return 1