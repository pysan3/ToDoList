import responder

api = responder.API(templates_dir='static')
api.add_route('/',  static=True, websocket=True)

@api.route('/api/login')
async def login(req, resp):
    pass

if __name__ == '__main__':
    api.run()