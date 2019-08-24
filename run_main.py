import responder
import random
import subprocess
import urllib

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
        resp.media = dict({'valid': '1', 'user_id': str(user_id), 'user_name': backapp.username(user_id)}, **backapp.load_file(user_id))
    else:
        resp.media = {'valid': '0'}

@api.route('/api/userfile/{file_url}')
async def user_file(req, resp, *, file_url):
    user_id = backapp.verify_user((await req.media())['token'])
    if user_id:
        with open(urllib.parse.unquote(file_url), 'r') as f:
            resp.text = f.read()
    else:
        resp.text = ''

@api.route('/api/fileupload/{file_url}')
async def fileupload(req, resp, *, file_url):
    data = await req.media()
    user_id = backapp.verify_user(data['token'])
    if user_id:
        with open(urllib.parse.unquote(file_url), 'w') as f:
            f.write(data['data'])

@api.route('/ws/terminal', websocket=True)
async def ws_terminal(ws):
    await ws.accept()
    user_id = backapp.verify_user((await ws.receive_json())['token'])
    try:
        while user_id is not False:
            data = await ws.receive_json()
            if user_id != backapp.verify_user(data['token']):
                break
            if len(data['command'].split()) > 0:
                res = subprocess.run(data['command'].split(), cwd=f'user_files/{user_id}', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                await ws.send_json({'result': res.stdout.decode('utf-8')})
    except:
        pass
    await ws.close()

@api.route('/api/random')
def random_number(req, resp):
    resp.media = {'randomNumber': random.randint(1, 100)}

if __name__ == '__main__':
    api.run()