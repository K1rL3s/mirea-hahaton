import socketio

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=['http://localhost:5173'],
)

sio_app = socketio.ASGIApp(socketio_server=sio)

@sio.event
async def connect(sid, environ):
    print(f"connect {sid}")
    raise Exception('hi')