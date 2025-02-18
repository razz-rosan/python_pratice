from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session 
from typing import List ,Optional
from .. import models, schema,utils ,oauth2
from .. databse import get_db
from .. import databse , schema ,models,utils ,oauth2
from sqlalchemy import func

router = APIRouter(
    prefix= "/posts",
    tags=['Posts']
)


@router.get("/",response_model= list[schema.Post])    
def get_posts(db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),limit:int = 10,skip:int = 0,search:Optional[str] = ""):
    print(limit)
    #cursor.execute("""select * from posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.post, func.count(models.vote.post_id).label("Votes")).join(models.vote,models.vote.post_id == models.Post.id,isouter= True).group_by(models.Post.id).all()
    
    return results


"""@app.post("/createpost")
def create_posts(new_post:post): 
    print(new_post)
    print(new_post.dict()) 
    return{"Data":"new Post"}
""" 

"""
app.post("/createpost")
def create_posts(payload: dict = Body(...)): ## in this passing parameter we use the variable name payload andassign it as a dictionary so that it wii take arguments as json format
   print(payload) ## this is used to get the data from the post man
  return{"new post":f"title :{payload['title']}  content: {payload['content']}"} 
"""
"""@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: post): 
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)# inserting a new post to the database {post_Dict}
    cursor.execute( IINSERT INTO post(title,content,published) VALUES(%s,%s,%s) RETURNING* ,(post.titlr,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": "created post"}
    """

@router.post("/",status_code=status.HTTP_201_CREATED, response_model= schema.Post)
def create_posts(post: schema.PostCreate,db:Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
 
    new_post = models.Post(owner_id = current_user.id,**post.dict())   #it is used to add as many para meter you want idk why it is nit working 
    #new_post = models.Post(title= post.title, content = post.content,published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

@router.get("/{id}",response_model= schema.Post) ##{id} it is a path parameter 
def get_post(id:int,db:Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)): #,response:Response use this when you use the response module 
    #cursor.execute("""Select * from posts Where id = %s """,(str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    
    return post

# deleting a post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform the action")

    post_query.delete(synchronize_session= False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update post
@router.put("/{id}",response_model= schema.Post)
def update_post(id:int,updated_post:schema.PostCreate,db:Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform the action")


    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()