from typing import Union

from fastapi import FastAPI

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "Title Post 1", "content": "Content of post 1", "id": 1},
            {"title": "Favorite Food", "content": "I like pizza", "id": 2}]


@app.get("/")
def read_root():
    return {"Hello": "Test"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}