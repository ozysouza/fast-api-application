from fastapi import FastAPI, Depends, Response, status, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from typing import Dict, Any, Type

from .database import create_db_and_tables, get_session
from . import schemas, models

ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables at app startup
    create_db_and_tables()
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_session)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_session)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_session)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} was not found!")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_session)) -> Response:
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id}, does not exist!")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_session)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id}, does not exist!")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
