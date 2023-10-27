from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"title": "title 1", "content": "content 1", "id": 1}, 
    {"title": "title 2", "content": "content 2", "id": 2}
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}
 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):

    # Testing the data points being posted by printing

    # print(post)
    # print(post.published)
    # print(post.rating)
    # print(post.dict())

    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)

    return{"data": post_dict}

# Function fetching all the data points in not so good way

# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return{"new_post": f"title => {payload['title']} | Content: {payload['content']}"}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1 ]
    return{"detail": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # print(id)
    post = find_post(int(id))
    # return {"post_detail": f"Here is your post {id}"}
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id {id} was not found" )
       
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    
    return {"post_detail": post  }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail= f"post with id {id} was not found" )
    

    my_posts.pop(index)
    return {"message": 'post was successfully deleted'}