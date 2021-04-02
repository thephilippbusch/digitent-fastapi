from fastapi import FastAPI, WebSocket, Body, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import time

from .connection_handler import ConnectionHandler

from .models.user_model import UserSchema, UserLoginSchema, UserIDModel
from .auth.auth_handler import signJWT
from .auth.auth_bearer import JWTBearer

from .db.test_db import TestManager
from .db.user_db import UserManager
from .db.chat_db import ChatManager

app = FastAPI()

handler = ConnectionHandler()

users = []

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

# Test call for initial setup, can be ignored
@app.get("/test", dependencies=[Depends(JWTBearer())], tags=["testing"])
async def get_test_response() -> dict:
    try:
        res = TestManager.get_message()
        if res:
            return {
                "status": 200,
                "message": "Successful",
                "data": res
            }
        else:
            return {
                "status": 400,
                "message": "Something went wrong"
            }
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Sign Up API endpoint
@app.post("/auth/register", tags=["auth"])
async def create_user(user: UserSchema = Body(...)):
    try:
        if UserManager.check_user(user):
            return {
                "status": 400,
                "message": "Email already in use"
            }
        res = UserManager.add_user(user)
        token = signJWT(user.email)
        return {
            "status": 200,
            "message": "User created successfully",
            "token": token,
            "data": res
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Login API endpoint
@app.post("/auth/login", tags=["auth"])
async def login_user(user: UserLoginSchema = Body(...)):
    try:
        if UserManager.check_user(user):
            res = UserManager.find_by_mail(user.email)
            token = signJWT(user.email)
            print(res)
            return {
                "status": 200,
                "message": "Login successful",
                "token": token,
                "data": res
            }
        else: 
            return {
                "status": 404,
                "message": f"User {user.email} not found!"
            }
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Get User Data Endpoint
@app.get("/user/all", dependencies=[Depends(JWTBearer())], tags=["user"])
async def get_user() -> dict:
    try:
        res = UserManager.find_all()
        if res:
            return {
                "status": 200,
                "message": "Successful",
                "data": res
            }
        else:
            return {
                "status": 404,
                "message": "There are no Users"
            }
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/user/id", dependencies=[Depends(JWTBearer())], tags=["user"])
async def get_user_by_id(id: dict = Body(...)):
    try:
        res = UserManager.find_by_id(id["id"])
        if res:
            return {
                "status": 200,
                "message": "Successful",
                "data": res
            }
        else:
            return {
                "status": 404,
                "message": "User not found"
            }
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")


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