from fastapi import FastAPI, WebSocket, Body, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import time, uuid
from app.connection_handler import ConnectionHandler

from .schemas.user_schema import UserSchema, UserLoginSchema, AddAdminSchema
from .schemas.message_schema import MessageSchema
from .schemas.chatbot_answer_schema import ChatbotAnswerSchema
from .schemas.chat_schema import ChatSchema

from .auth.auth_handler import signJWT
from .auth.auth_bearer import JWTBearer

from .postgres.pgql_user import UserManager
from .postgres.pgql_message import MessageManager
from .postgres.pgql_chatbot_answers import ChatbotAnswerManager
from .postgres.pgql_chat import ChatManager

app = FastAPI()
handler = ConnectionHandler()

origins = [
    'localhost:3000',
    'http://localhost:3000',
    'praxi-chatbot-react.herokuapp.com',
    'https://praxi-chatbot-react.herokuapp.com'
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
async def get_test_response(message: str):
    return {
        "status": 200,
        "message": message
    }


# Sign Up API endpoint
@app.post("/auth/register", tags=["auth"])
async def create_user(user: UserSchema = Body(...)):
    try:
        id = uuid.uuid4()
        res = UserManager.insert_user(user, str(id))
        if res:
            token = signJWT(user.email)
            return {
                "status": 200,
                "message": "Successful",
                "token": token,
                "data": {
                    "_id": id
                }
            }
        else:
            return {
                "status": 400,
                "message": "Error while creating new User!"
            }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /auth/register")


# Login API endpoint
@app.post("/auth/login", tags=["auth"])
async def login_user(user: UserLoginSchema = Body(...)):
    try:
        res = UserManager.check_login(user)
        if res["successful"]:
            token = signJWT(user.email)
            return {
                "status": 200,
                "message": "Login successful",
                "token": token,
                "data": res["user"]
            }
        else: 
            return {
                "status": 404,
                "message": res["message"]
            }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /auth/login")


# Create Admin User endpoint
@app.post("/auth/admin", dependencies=[Depends(JWTBearer())], tags=["auth"])
async def make_admin(user: AddAdminSchema = Body(...)):
    try:
        res = UserManager.make_admin(user)
        if res["successful"]:
            return {
                "status": 200,
                "message": "Successful",
                "data": {
                    "_id": res["data"]["_id"],
                    "email": res["data"]["email"],
                    "username": res["data"]["username"],
                    "admin": res["data"]["admin"],
                }
            }
        else:
            return {
                "status": 400,
                "message": res["message"]
            }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /auth/admin")


# Get all User Endpoint
@app.get("/user/all", dependencies=[Depends(JWTBearer())], tags=["user"])
async def get_user():
    try:
        user_list = UserManager.get_all()
        if user_list:
            res = []
            for user in user_list:
                res.append({
                    "_id": user["_id"],
                    "email": user["email"],
                    "username": user["username"],
                    "admin": user["admin"]
                })
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
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /user/all")


# Get User by ID Endpoint
@app.get("/user/id", dependencies=[Depends(JWTBearer())], tags=["user"])
async def get_user_by_id(id: str):
    try:
        res = UserManager.get_user_by_id(id)
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
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /user/id")


# Get User by Email Endpoint
@app.get("/user/email", dependencies=[Depends(JWTBearer())], tags=["user"])
async def get_user_by_email(email: str):
    try:
        res = UserManager.get_user_by_mail(email)
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
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /user/id")


@app.get("/user/get_contact_details", dependencies=[Depends(JWTBearer())], tags=["user"])
async def get_contact_details(id: str):
    try:
        res = UserManager.get_contact_list(id)
        if res:
            if "status" in res:
                return {
                    "status": 404,
                    "message": "No Contacts found"
                }
            return {
                "status": 200,
                "message": "Successful",
                "data": res
            }
        return {
            "status": 400,
            "message": "Something went while fetching from the database"
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /user/get_contact_emails")


@app.post("/user/add_contact", dependencies=[Depends(JWTBearer())], tags=["user"])
async def add_contact(data: dict):
    try:
        res = UserManager.add_contact(data["user_id"], data["contact_email"])
        if res["successful"]:
            return {
                "status": 200,
                "message": "Successful",
                "data": res["data"]
            }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /user/add_contact")


# Create Message endpoint
@app.post("/messages/add", dependencies=[Depends(JWTBearer())], tags=["messages"])
async def add_message(message: MessageSchema = Body(...)):
    try:
        mid = uuid.uuid4()
        res = MessageManager.add_message(message, str(mid))
        if res:
            return {
                "status": 200,
                "message": "Successful"
            }
        else:
            return {
                "status": 400,
                "message": "Could not add message to Database"
            }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /messages/add")


# Get Messages by Chat endpoint
@app.get("/messages/all", dependencies=[Depends(JWTBearer())], tags=["messages"])
async def get_messages_by_chat(chat_id: str):
    try:
        message_list = MessageManager.get_messages_by_chat(chat_id)
        if message_list:
            res = []
            for message in message_list:
                res.append({
                    "_id": message["_id"],
                    "from_user": message["from_user"],
                    "chat_id": message["chat_id"]
                })
            return {
                "status": 200,
                "message": "Successful",
                "data": res
            }
        else:
            return {
                "status": 404,
                "message": "There are no Messages"
            }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /messages/all")


# Create Chatbot Answer endpoint
@app.post("/chatbot-answers/create", dependencies=[Depends(JWTBearer())], tags=["chatbot answers"])
async def create_chatbot_answer(chatbot_answer: ChatbotAnswerSchema = Body(...)):
    try:
        caid = uuid.uuid4()
        res = ChatbotAnswerManager.add_answer(chatbot_answer, str(caid))
        if res:
            return {
                "status": 200,
                "message": "Successful"
            }
        else:
            return {
                "status": 400,
                "message": "Could not add message to Database"
            }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /chatbot-answers/create")


# Get all Chatbot Answers created by an Admin
@app.get("/chatbot-answers/get-by-creator", dependencies=[Depends(JWTBearer())], tags=["chatbot answers"])
async def get_answers_by_creator(creator: str):
    try:
        res = ChatbotAnswerManager.get_messages_by_creator(creator)
        if res:
            data = []
            for answer in res:
                data.append({
                    "trigger": answer["trigger"],
                    "message": answer["message"],
                    "created_by": answer["created_by"],
                    "responses": answer["responses"]
                })
            return {
                "status": 200,
                "message": "Successful",
                "data": data
            }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /chatbot-answers/get-by-creator")


@app.post("/chats/get-chat-by-user-contact", dependencies=[Depends(JWTBearer())], tags=["chat"])
async def get_chat_by_user_contact(users: dict):
    try:
        res = ChatManager.get_chat_by_user_contact(users["user_id"], users["contact_id"])
        if res:
            return {
                "status": 200,
                "message": "Successful",
                "data": res
            }
        return {
            "status": 404,
            "message": "No chat found"
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /chats/get-chat-by-user-contact")


@app.post("/chats/new_chat", dependencies=[Depends(JWTBearer())], tags=["chat"])
async def create_new_chat(chat: ChatSchema = Body(...)):
    try:
        id = uuid.uuid4()
        res = ChatManager.add_chat(chat, id)
        if res:
            return {
                "status": 200,
                "message": "Successful",
                "data": id
            }
        else:
            return {
                "status": 400,
                "message": "Error inserting data into database"
            }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error @ /chats/new_chat")


@app.websocket("/ws/{channel}")
async def chat(ws: WebSocket, channel: str):
    try:
        await handler.connect(ws, channel)
        
        while True:
            data = await ws.receive_json()
            if data:
                await handler.send_to_room({
                    "message": data["message"],
                    "from": data["user"]
                }, channel)
            
    except Exception as e:
        print(e)


@app.websocket("/praxi/{channel}")
async def praxi_chat(ws: WebSocket, channel: str):
    try:
        await ws.accept()
        await ws.send_json({
            "message": "Hi, ich bin Praxi! Dein Persönlicher Assistent für deine Praxisphase. Wie kann ich dir helfen?",
            "from": "bot"
        })
        
        while True:
            data = await ws.receive_json()
            print(data)
            if data:
                await ws.send_json({
                    "message": data["message"],
                    "from": data["user"]
                })
            answer = ChatbotAnswerManager.get_answer_by_trigger(data["message"])
            time.sleep(1)
            if answer:
                if 'responses' in answer:
                    await ws.send_json({
                        "message": answer["message"],
                        "from": "bot",
                        "answers": answer["responses"]
                    })
                else:
                    await ws.send_json({
                        "message": answer["message"],
                        "from": "bot"
                    })
            else:
                await ws.send_json({
                    "message": "Leider kann ich dir dazu nicht antworten!",
                    "from": "bot",
                })
            
    except Exception as e:
        print(e)