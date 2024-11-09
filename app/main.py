from fastapi import FastAPI, Depends, Response, status, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from typing import Dict, Any

from .database import create_db_and_tables, get_session
from .models import Post

ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables at app startup
    create_db_and_tables()
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/posts")
def get_posts(db: Session = Depends(get_session)) -> Dict[str, Any]:
    posts = db.query(Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_session)) -> Dict[str, Any]:
    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_posts(id: int, db: Session = Depends(get_session)) -> Dict[str, Any]:
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} was not found!")
    return {"more_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_session)) -> Response:
    post = db.query(Post).filter(Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id}, does not exist!")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_session)) -> Dict[str, Any]:
    post_query = db.query(Post).filter(Post.id == id)

    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id}, does not exist!")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
