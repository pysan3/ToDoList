import responder

api = responder.API()
api.add_route('/',  static=True, websocket=True)

@api.route('/api/login')
async def login(req, resp):
    pass