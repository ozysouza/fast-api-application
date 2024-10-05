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


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randint(3, 10000)
    my_posts.append(post_dict)
    return {"data": post_dict}
