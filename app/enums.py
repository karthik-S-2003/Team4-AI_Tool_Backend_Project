from enum import Enum

class PricingType(str, Enum):
    FREE = "Free"
    PAID = "Paid"
    SUBSCRIPTION = "Subscription"


class ReviewStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class CategoryType(str, Enum):
    NLP = "NLP"
    COMPUTER_VISION = "Computer Vision"
    DEV_TOOLS = "Dev Tools"
    PRODUCTIVITY = "Productivity"
