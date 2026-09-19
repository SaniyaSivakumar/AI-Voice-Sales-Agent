from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ProductSchema(BaseModel):
    id: int
    name: str
    category: str
    price: float
    description: str
    features: List[str]
    availability: str
    stock_quantity: int
    discount_percentage: float = 0.0
    discounted_price: float
    is_in_stock: bool

class ProductAvailabilityResponse(BaseModel):
    product_id: int
    name: str
    availability: str
    stock_quantity: int
    is_in_stock: bool
    status_message: str

class IntentQueryRequest(BaseModel):
    intent: str = Field(..., description="Detected customer intent (e.g., price_query, availability, product_search)")
    query: Optional[str] = Field(None, description="Search query or product name extracted from user transcript")
    product_id: Optional[int] = Field(None, description="Optional target product ID")
    category: Optional[str] = Field(None, description="Optional product category filter")

class IntentQueryResponse(BaseModel):
    intent: str
    spoken_response: str
    products: List[ProductSchema] = []
    meta: Dict[str, Any] = {}
