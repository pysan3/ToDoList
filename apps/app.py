import numpy as np
import os
import subprocess
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

def load_file(user_id, project):
    path = f'user_files/{user_id}/{project}'
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

def load_project(user_id):
    path = f'user_files/{user_id}'
    if not os.path.exists(path):
        os.mkdir(path)
    dirs = []
    for d in os.listdir(path):
        d_path = f'{path}/{d}'
        if os.path.isdir(d_path):
            dirs.append({'name': d})
    return {'projects': dirs}

def username(user_id):
    session = Session()
    name = session.query(Users).filter_by(id=user_id).first()
    session.close()
    return name.user_name

def run_command(user_id, project, command):
    in_file = subprocess.PIPE
    out_file = subprocess.PIPE
    project_path = f'user_files/{user_id}/{project}/'
    command_length = len(command)
    for i, c in enumerate(reversed(command), 1):
        index = command_length - i
        if c == '>':
            out_file = open(project_path + command[index + 1], 'w')
            command = command[:index]
        elif c == '>>':
            out_file = open(project_path + command[index + 1], 'a')
            command = command[:index]
        elif c == '<':
            in_file = open(project_path + command[index + 1], 'r')
            command = command[:index]
        elif c == '|':
            in_file = run_command(user_id, command[:index])
            command = command[index + 1:]
            break
    return subprocess.run(command, cwd=project_path, stdin=in_file, stdout=out_file, stderr=out_file).stdout
