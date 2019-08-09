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

@api.route('/api/loggedin/{user_id}')
async def logged_in(req, resp, *, user_id):
    resp.text = f"{backapp.check_login(int(user_id))}"

@api.route('/api/random')
def random_number(req, resp):
    resp.media = {'randomNumber': random.randint(1, 100)}

if __name__ == '__main__':
    api.run()