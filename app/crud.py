from sqlalchemy.orm import Session
from app.models import AITool, Review
import uuid
from sqlalchemy import func


def get_tools(db: Session, category=None, pricing_type=None, rating_gte=None):
    query = db.query(AITool)
    if category:
        query = query.filter(AITool.category == category)
    if pricing_type:
        query = query.filter(AITool.pricing_type == pricing_type)
    if rating_gte:
        query = query.filter(AITool.average_rating >= rating_gte)
    return query.all()

def create_tool(db: Session, tool_data):
    existing_tool = db.query(AITool).filter(
        AITool.name == tool_data.name,
       
        AITool.category == tool_data.category,
        AITool.pricing_type == tool_data.pricing_type
    ).first()

    if existing_tool:
        return None 
    tool = AITool(
        id=str(uuid.uuid4()),
        **tool_data.model_dump()
    )

    db.add(tool)
    db.commit()
    db.refresh(tool)
    return tool

def update_tool(db: Session, tool_id: str, tool_data):
    tool = db.query(AITool).filter(AITool.id == tool_id).first()
    if not tool:
        return None
    for key, value in tool_data.dict(exclude_unset=True).items():
        setattr(tool, key, value)
    db.commit()
    db.refresh(tool)
    return tool

def delete_tool(db: Session, tool_id: str):
    tool = db.query(AITool).filter(AITool.id == tool_id).first()
    if not tool:
        return False
    db.delete(tool)
    db.commit()
    return True

# Reviews
def create_review(db: Session, review_data):
    review = Review(id=str(uuid.uuid4()), status="Pending", **review_data.dict())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def approve_review(db: Session, review_id: str):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        return None
    review.status = "Approved"
    db.commit()
    avg = db.query(func.avg(Review.rating)).filter(
        Review.tool_id == review.tool_id, Review.status == "Approved"
    ).scalar()
    tool = db.query(AITool).filter(AITool.id == review.tool_id).first()
    tool.average_rating = avg
    db.commit()
    db.refresh(tool)
    return review

def reject_review(db: Session, review_id: str):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        return None
    review.status = "Rejected"
    db.commit()
    return review

def get_approved_reviews(db: Session, tool_id: str | None = None):
    query = db.query(Review).filter(Review.status == "Approved")

    if tool_id:
        query = query.filter(Review.tool_id == tool_id)

    return query.all()
