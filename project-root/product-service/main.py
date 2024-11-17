# product-service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import motor.motor_asyncio
import os

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client.ecommerce

class Product(BaseModel):
    name: str
    price: float
    description: str
    stock: int

@app.get("/products", response_model=List[Product])
async def get_products():
    products = []
    cursor = db.products.find()
    async for document in cursor:
        products.append(Product(**document))
    return products

@app.get("/products/{product_id}")
async def get_product(product_id: str):
    product = await db.products.find_one({"_id": product_id})
    if product:
        return Product(**product)
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products")
async def create_product(product: Product):
    result = await db.products.insert_one(product.dict())
    return {"id": str(result.inserted_id)}
