from fastapi import WebSocket
from typing import List 

class ConnectionHandler:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    async def broadcast(self, message: dict):
        for connection in self.connections:
            await connection.send_json(message)
