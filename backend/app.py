from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os

from database import (
    init_db,
    search_products_db,
    get_product_by_id_db,
    get_product_by_name_db,
    get_categories_db
)
from schema import (
    ProductSchema,
    ProductAvailabilityResponse,
    IntentQueryRequest,
    IntentQueryResponse
)

# Initialize FastAPI application
app = FastAPI(
    title="AI Voice Sales Agent - Backend API",
    description="Product Database & Query REST API for AI Voice Sales Agent integration.",
    version="1.0.0"
)

# Enable CORS for frontend and voice module integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db():
    """Initializes database schema and seed data on server startup."""
    init_db()

@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "AI Voice Sales Agent Backend API",
        "docs_url": "/docs"
    }

# -------------------------------------------------------------------
# 1. PRODUCT SEARCH API
# -------------------------------------------------------------------
@app.get("/api/products/search", response_model=List[ProductSchema], tags=["Products"])
def search_products(
    q: Optional[str] = Query(None, description="Search keyword in product name, description, features"),
    category: Optional[str] = Query(None, description="Filter by category name"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    in_stock_only: bool = Query(False, description="Set to true to show only available products")
):
    """
    Product Search API:
    Searches products by keyword query, category, price range, or stock status.
    """
    products = search_products_db(
        query=q,
        category=category,
        min_price=min_price,
        max_price=max_price,
        in_stock_only=in_stock_only
    )
    return products

@app.get("/api/products", response_model=List[ProductSchema], tags=["Products"])
def get_all_products(
    category: Optional[str] = Query(None, description="Filter products by category")
):
    """Retrieves all products from the database catalog."""
    return search_products_db(category=category)

@app.get("/api/categories", response_model=List[str], tags=["Products"])
def get_categories():
    """Retrieves all distinct product categories in stock."""
    return get_categories_db()

# -------------------------------------------------------------------
# 2. PRODUCT DETAILS API
# -------------------------------------------------------------------
@app.get("/api/products/details/by-name", response_model=ProductSchema, tags=["Products"])
def get_product_details_by_name(
    name: str = Query(..., description="Product name or keyword search")
):
    """
    Product Details API (by Name/Query):
    Retrieves complete metadata for a product by searching its name.
    """
    product = get_product_by_name_db(name)
    if not product:
        raise HTTPException(status_code=404, detail=f"No product found matching '{name}'.")
    return product

@app.get("/api/products/{product_id}", response_model=ProductSchema, tags=["Products"])
def get_product_details(product_id: int):
    """
    Product Details API (by ID):
    Retrieves full details for a product by its unique product ID.
    """
    product = get_product_by_id_db(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
    return product

# -------------------------------------------------------------------
# 3. PRODUCT AVAILABILITY API
# -------------------------------------------------------------------
@app.get("/api/products/{product_id}/availability", response_model=ProductAvailabilityResponse, tags=["Availability"])
def check_product_availability_by_id(product_id: int):
    """
    Product Availability API (by ID):
    Checks stock quantity and availability status for a specific product ID.
    """
    product = get_product_by_id_db(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
    
    in_stock = product["is_in_stock"]
    qty = product["stock_quantity"]
    avail_str = product["availability"]
    
    if in_stock:
        msg = f"'{product['name']}' is in stock ({qty} units available)."
    else:
        msg = f"Sorry, '{product['name']}' is currently out of stock."

    return {
        "product_id": product["id"],
        "name": product["name"],
        "availability": avail_str,
        "stock_quantity": qty,
        "is_in_stock": in_stock,
        "status_message": msg
    }

@app.get("/api/products/availability/search", response_model=ProductAvailabilityResponse, tags=["Availability"])
def check_product_availability_by_search(
    name: str = Query(..., description="Product name or query to check availability")
):
    """
    Product Availability API (by Name/Query):
    Checks if a product is in stock based on product name or search query.
    """
    product = get_product_by_name_db(name)
    if not product:
        raise HTTPException(status_code=404, detail=f"No product matching '{name}' found.")
    
    in_stock = product["is_in_stock"]
    qty = product["stock_quantity"]
    avail_str = product["availability"]
    
    if in_stock:
        msg = f"Yes, '{product['name']}' is available ({qty} units in stock)."
    else:
        msg = f"Currently, '{product['name']}' is out of stock."

    return {
        "product_id": product["id"],
        "name": product["name"],
        "availability": avail_str,
        "stock_quantity": qty,
        "is_in_stock": in_stock,
        "status_message": msg
    }

# -------------------------------------------------------------------
# 4. INTENT INTEGRATION ENDPOINT (For DL Model & Voice Module)
# -------------------------------------------------------------------
@app.post("/api/intent-query", response_model=IntentQueryResponse, tags=["AI Integration"])
def process_intent_query(payload: IntentQueryRequest):
    """
    Integration API:
    Receives classified intent from Padma's DL Model / Voice Module and returns
    relevant product data and ready-to-speak responses for Text-to-Speech (TTS).
    """
    intent = payload.intent.lower().strip()
    query = payload.query or ""
    
    if intent in ["product_search", "search"]:
        results = search_products_db(query=query)
        if results:
            names = ", ".join([p["name"] for p in results[:3]])
            speech = f"I found {len(results)} products. Here are top options: {names}."
        else:
            speech = f"I couldn't find any products matching '{query}'."
        return {"intent": intent, "spoken_response": speech, "products": results}

    elif intent in ["price_query", "price"]:
        product = get_product_by_name_db(query) if query else None
        if product:
            price = product["price"]
            disc = product["discount_percentage"]
            if disc > 0:
                speech = f"The price of {product['name']} is ${price:.2f}, but it is currently on sale for ${product['discounted_price']:.2f}."
            else:
                speech = f"The {product['name']} costs ${price:.2f}."
            return {"intent": intent, "spoken_response": speech, "products": [product]}
        else:
            results = search_products_db(query=query)
            if results:
                speech = f"Here is the price for {results[0]['name']}: ${results[0]['price']:.2f}."
                return {"intent": intent, "spoken_response": speech, "products": results[:1]}
            speech = f"I couldn't find pricing information for '{query}'."
            return {"intent": intent, "spoken_response": speech, "products": []}

    elif intent in ["availability", "stock"]:
        product = get_product_by_name_db(query) if query else None
        if product:
            if product["is_in_stock"]:
                speech = f"Yes, {product['name']} is currently in stock with {product['stock_quantity']} units available."
            else:
                speech = f"Sorry, {product['name']} is currently out of stock."
            return {"intent": intent, "spoken_response": speech, "products": [product]}
        speech = f"I couldn't check availability for '{query}'."
        return {"intent": intent, "spoken_response": speech, "products": []}

    elif intent in ["product_recommendation", "recommendation"]:
        results = search_products_db(query=query)
        if not results:
            results = search_products_db(in_stock_only=True)
        top_items = results[:2]
        if top_items:
            names = " and ".join([p["name"] for p in top_items])
            speech = f"I highly recommend checking out {names}."
        else:
            speech = "We have great items in stock, what category are you interested in?"
        return {"intent": intent, "spoken_response": speech, "products": top_items}

    elif intent == "greeting":
        return {
            "intent": intent,
            "spoken_response": "Hello! Welcome to our store. How can I help you find what you are looking for today?",
            "products": []
        }

    elif intent == "goodbye":
        return {
            "intent": intent,
            "spoken_response": "Thank you for visiting! Have a wonderful day!",
            "products": []
        }

    # Default fallback
    results = search_products_db(query=query)
    return {
        "intent": intent,
        "spoken_response": f"Here are the items matching your query '{query}'.",
        "products": results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
