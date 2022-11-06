from .. import models, schemas, utils, oauth2
from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["vote"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    """
    Vote for a post
    """

    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} already voted for this post"
            )

        new_vote = models.Vote(
            post_id=vote.post_id,
            user_id=current_user.id,
        )

        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote does not exist"
            )

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Voted deleted successfully"}
