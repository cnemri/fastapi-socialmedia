from .. import models, schemas, oauth2
from fastapi import Response, status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).offset(skip).limit(limit).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(
            models.Post.title.contains(search)).group_by(models.Post.id).all()

    return results


@ router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    post_dict = post.dict()
    new_post = models.Post(owner_id=current_user.id, **post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@ router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(
            models.Post.id == id).group_by(models.Post.id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@ router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = query.first()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post with id {} not found'.format(id))

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')

    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ router.put('/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = query.first()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post with id {} not found'.format(id))

    if updated_post.owner_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN, detail = 'Not enough permissions')

    query.update(post.dict(), synchronize_session = False)
    db.commit()
    db.refresh(updated_post)
    return updated_post
