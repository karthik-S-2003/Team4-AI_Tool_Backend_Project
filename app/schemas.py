from pydantic import BaseModel,ConfigDict
from typing import Optional
from enum import Enum

class PricingType(str, Enum):
    Free = "Free"
    Paid = "Paid"
    Subscription = "Subscription"

class ReviewStatus(str, Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"

class ReviewBase(BaseModel):
    tool_id: str
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: str
    status: ReviewStatus

    model_config = ConfigDict(
        from_attributes=True
    )
   

class AIToolBase(BaseModel):
    name: str
    use_case: Optional[str] = None
    category: Optional[str] = None
    pricing_type: PricingType

class AIToolCreate(AIToolBase):
    pass

class AITool(AIToolBase):
    id: str
    average_rating: float
    model_config = ConfigDict(
        from_attributes=True
    )
   

