from fastapi import FastAPI, Depends, HTTPException, Query , APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.database import Base, engine, SessionLocal
import app.models as models, app.schemas as schemas, app.crud as crud
from app.auth import authenticate_admin, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_admin
from ..database import get_db



router = APIRouter(prefix="/users",tags=['Users'])
# ---- Public APIs ----
@router.get("/tools", response_model=list[schemas.AITool])
def list_tools(
    category: str = None,
    pricing_type: schemas.PricingType = None,
    rating_gte: float = Query(None, alias="rating"),
    db: Session = Depends(get_db)
):
    return crud.get_tools(db, category, pricing_type, rating_gte)

@router.post("/review", response_model=schemas.Review)
def submit_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db, review)