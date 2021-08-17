from typing import Optional
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get('/')
def index(limit:int , published:bool, sort: Optional[str] = None):
    
    if published:
        return {'data': f'{limit}published blogs from the db'}
    else:
        return {'data': f'{limit}blogs from the db'}
    

@app.get('/blog/unpublished')
def unbuplished():
    return {'data': 'unpublished'}

@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}



@app.get('/blog/{id}/comments')
def comments(id):
    return {'data': 'comments'}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]



@app.post('/blog')
def createblog(request:Blog):
    
    return {'data': f'Blog is created with title {request.title}'}

