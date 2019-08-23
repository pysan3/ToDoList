import responder
import sqlite3

import random

import apps.app as backapp

api = responder.API(static_dir='./static', templates_dir='./static')
api.add_route('/', static=True, websocket=True)

@api.route('/api/login')
async def login(req, resp):
    resp.media = backapp.login(await req.media())

@api.route('/api/signup')
async def signup(req, resp):
    resp.media = backapp.signup(await req.media())

@api.route('/api/loggedin')
async def logged_in(req, resp):
    resp.text = 'valid' if backapp.check_login((await req.media())['token']) else 'invalid'

@api.route('/api/loadfile')
async def load_file(req, resp):
    user_id = backapp.verify_user((await req.media())['token'])
    if user_id:
        resp.media = dict({
            'valid': '1',
            'user_name': backapp.username(user_id)
        }, **backapp.load_file(user_id))
    else:
        resp.media = {'valid': '0'}

@api.route('/api/random')
def random_number(req, resp):
    resp.media = {'randomNumber': random.randint(1, 100)}

if __name__ == '__main__':
    api.run()