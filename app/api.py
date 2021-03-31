from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import time
from .connection_handler import ConnectionHandler

app = FastAPI()

handler = ConnectionHandler()

origins = [
    'localhost:3000',
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/login", tags=["login"])
async def get_test_response() -> dict:
    return {"message": "Hello World!"}

@app.websocket('/ws')
async def websocket_endpoint(ws: WebSocket):
    await handler.connect(ws)
    while True:
        data = await ws.receive_text()
        print(data)
        await ws.send_json({
            "message": data,
            "from": "user"
        })
        time.sleep(1)

        await handler.broadcast({
            "message": "Gerichtet an alle: habt ihr die Frage bekommen?",
            "from": "bot",
            "answers": [
                "Ja",
                "Nein"
            ]
        })

        # await handler.broadcast({
        #     "message": "Hallo! Wie Geht es dir?",
        #     "from": "bot",
        #     "answers": [
        #         "Ganz gut",
        #         "Mäßig",
        #         "Richtig Kacke"
        #     ]
        # })