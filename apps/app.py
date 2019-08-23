import numpy as np
import os
import hashlib
import secrets
from datetime import datetime

from apps.database import Session, Users, TokenTable
from sqlalchemy.sql import exists

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
    return {'isFound': len(user), 'token': new_token(user_id), 'msg': msg}

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
    return {'isFound': (user_id >= 0) + 0, 'token': new_token(user_id), 'msg': msg}

def check_login(token):
    if token == 'none':
        return False
    session = Session()
    check = session.query(exists().where(TokenTable.token==token))
    session.close()
    return check

def new_token(user_id):
    session = Session()
    token = secrets.token_hex()
    session.add(TokenTable(
        token=token,
        user_id=user_id
    ))
    session.commit()
    session.close()
    return token

def verify_user(token):
    session = Session()
    user_id = session.query(TokenTable).filter_by(token=token).one_or_none()
    session.close()
    if user_id is None:
        return False
    else:
        return int(user_id.user_id)

def load_file(user_id):
    path = f'user_files/{user_id}'
    if not os.path.exists(path):
        os.mkdir(path)
    def file_recursive(path):
        files = []
        for f in os.listdir(path):
            f_path = f'{path}/{f}'
            f_data = {'id': f_path, 'name': f, 'type': 'file', 'show': '1', 'insides': []}
            if os.path.isdir(f_path):
                f_data['type'] = 'dir'
                f_data['insides'].extend(file_recursive(f_path))
            files.append(f_data)
        return files
    return {'comment': file_recursive(path)}

def username(user_id):
    session = Session()
    name = session.query(Users).filter_by(id=user_id).first()
    session.close()
    return name.user_name