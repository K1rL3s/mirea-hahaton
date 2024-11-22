import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.socket import sio
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from app.routes import include_routers
from di.container import make_container
import socketio

from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:5173"],  # Adjust this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/ws', socketio.ASGIApp(sio, socketio_path='/ws/socket.io'))

@sio.event
def connect(sid, environ):
    print('connect', sid)

def create_app() -> FastAPI:
    include_routers(app)
    container = make_container(extra_providers=[FastapiProvider()])
    setup_dishka(container, app)
    return app