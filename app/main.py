from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'postgres', user = 'postgres',
                                password = 'haslo1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was succesfull')
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error :", error)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return post

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
