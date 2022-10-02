from collections import defaultdict
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, WebSocket, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from database.db import engine
from starlette.websockets import WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from routers.user import router as user_router
from database import models
from authentication.auth import get_current_user_from_token
from schemas import UserAuth


app = FastAPI()

app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    """
        Manages chat room sessions and members along with message routing
    """

    def __init__(self):
        self.connections: dict = defaultdict(dict)

    def get_members(self, room_name):
        try:
            return self.connections[room_name]
        except Exception:
            return None

    async def connect(self, websocket: WebSocket, room_name: str):
        await websocket.accept()
        if self.connections[room_name] == {} or len(self.connections[room_name]) == 0:
            self.connections[room_name] = []
        self.connections[room_name].append(websocket)


    def remove(self, websocket: WebSocket, room_name: str):
        self.connections[room_name].remove(websocket)


    async def send_private_message(self, message: str, room_name: str):

        living_connections = []
        
        while len(self.connections[room_name]) > 0:

            websocket = self.connections[room_name].pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        
        self.connections[room_name] = living_connections


manager = ConnectionManager()

# controller routes
@app.get("/{room_name}/{user_name}")
async def get(request: Request, room_name, user_name):
    return templates.TemplateResponse(
        "chat_room.html",
        {"request": request, "room_name": room_name, "user_name": user_name},
    )


@app.websocket("/ws/{room_name}")
async def websocket_endpoint(
    websocket: WebSocket, room_name, background_tasks: BackgroundTasks
):
    await manager.connect(websocket, room_name)
    try:
        while True:
            data = await websocket.receive_text()

            room_members = (
                manager.get_members(room_name)
                if manager.get_members(room_name) is not None
                else []
            )
            if websocket not in room_members:
                print("SENDER NOT IN ROOM MEMBERS: RECONNECTING")
                await manager.connect(websocket, room_name)

            await manager.send_private_message(f"{data}", room_name)
    except WebSocketDisconnect:
        manager.remove(websocket, room_name)
