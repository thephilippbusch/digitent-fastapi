import uvicorn
from pymongo import MongoClient
import logging

client = MongoClient(host="localhost", port=27017)

db = client["chat_bot"]

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0')
