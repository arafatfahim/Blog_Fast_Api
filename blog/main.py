from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session, session
from . import schemas, models
from .database import engine, SessionLocal
import blog

app = FastAPI()


models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#create post
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db : Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



#delete post
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db:session =Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'deleted'

#update
@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db:session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
             detail= f'there is no blog by this id ({id})')
    blog.update(request)
    db.commit()
    return 'Successfully updated'


#get all post
@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

#seach post by id
@app.get('/blog/{id}', status_code=200)
def show(id, response: Response, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with this id ({id}) is not available at this momment')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'details':f'Blog with this id ({id}) is not available at this momment' }   
    return blog
