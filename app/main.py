from typing import Annotated
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Product(BaseModel):
    name: str
    price: float = Field(gt=0, description="The price must be greater than zero")
    in_stock: bool
    description: str | None = Field(
        default=None, max_length=300, title="Description of the product"
    )
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    products: list[Product]


@app.get("/")
async def root():
    return {"message": "Welcome To Kenya"}


@app.post("/products/")
async def create_product(product: Product):
    product_dict = product.model_dump()
    if product.tax:
        product_with_tax = product.price + product.tax
        product_dict.update({"price_with_tax": product_with_tax})
    return product_dict


@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    return {"product_id": product_id, **product.model_dump()}


@app.get("/products/")
async def read_products(q: Annotated[list[str] | None, Query()] = None):
    results = {"products": [{"product_id": "foo"}, {"product_id": "bar"}]}
    if q:
        results.update({"q": q})
    return results


# Offer routes
@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer
