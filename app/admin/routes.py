
from fastapi import FastAPI, Depends, HTTPException, Query , APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.database import Base, engine, SessionLocal
import app.models as models, app.schemas as schemas, app.crud as crud
from app.auth import authenticate_admin, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_admin
from ..database import get_db

router = APIRouter(prefix='/admin',tags=['Admin'])


@router.post("/login")
def admin_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": admin.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/tools", response_model=schemas.AITool)
def add_tool(
    tool: schemas.AIToolCreate,
    db: Session = Depends(get_db),
    admin: models.Admin = Depends(get_current_admin)
):
    created_tool = crud.create_tool(db, tool)

    if not created_tool:
        raise HTTPException(
            status_code=400,
            detail="Tool already exists with same details"
        )

    return created_tool

@router.put("/tools/{tool_id}", response_model=schemas.AITool)
def edit_tool(tool_id: str, tool: schemas.AIToolCreate, db: Session = Depends(get_db), admin: models.Admin = Depends(get_current_admin)):
    updated_tool = crud.update_tool(db, tool_id, tool)
    if not updated_tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return updated_tool

@router.delete("/tools/{tool_id}")
def delete_tool(tool_id: str, db: Session = Depends(get_db), admin: models.Admin = Depends(get_current_admin)):
    if not crud.delete_tool(db, tool_id):
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"detail": "Tool deleted"}

@router.get("/reviews", response_model=list[schemas.Review])
def list_reviews(status: str = None, tool_id: str = None, db: Session = Depends(get_db), admin: models.Admin = Depends(get_current_admin)):
    query = db.query(models.Review)
    if status:
        query = query.filter(models.Review.status == status)
    if tool_id:
        query = query.filter(models.Review.tool_id == tool_id)
    return query.all()

@router.patch("/reviews/{review_id}/approve", response_model=schemas.Review)
def approve_review(review_id: str, db: Session = Depends(get_db), admin: models.Admin = Depends(get_current_admin)):
    review = crud.approve_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.patch("/reviews/{review_id}/reject", response_model=schemas.Review)
def reject_review(review_id: str, db: Session = Depends(get_db), admin: models.Admin = Depends(get_current_admin)):
    review = crud.reject_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review
