from typing import Annotated
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field, HttpUrl, Form

app = FastAPI()


class FormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}


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
    images: list[Image] | None = Field(
        default=None,
        max_items=10,
        examples=[
            {"url": "https://example.com/image1.jpg", "name": "Image 1"},
        ],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "price": 50.2,
                    "in_stock": True,
                    "description": "Foo product",
                    "images": [
                        {"url": "https://example.com/image1.jpg", "name": "Image 1"},
                        {"url": "https://example.com/image2.jpg", "name": "Image 2"},
                    ],
                    "tax": 1.5,
                }
            ]
        }
    }


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    products: list[Product]


@app.get("/")
async def root():
    return {"message": "Welcome To Kenya"}


# Auth routes
@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data


# Image routes
@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images


# Product routes
@app.post("/products/")
async def create_product(product: Product):
    product_dict = product.model_dump()
    if product.tax:
        product_with_tax = product.price + product.tax
        product_dict.update({"price_with_tax": product_with_tax})
    return product_dict


@app.patch("/products/{product_id}")
async def update_product(product_id: str, product: Product):
    return {"product_id": product_id, **product.model_dump(exclude_unset=True)}


@app.get("/products/")
async def read_products(q: Annotated[list[str] | None, Query()] = None):
    results = {"products": [{"product_id": "foo"}, {"product_id": "bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/products/{product_id}")
async def read_product(product_id: str):
    return {"product_id": product_id}


# Offer routes
@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer
