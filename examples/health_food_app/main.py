from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Global Korean Health Food App")


class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str


class Order(BaseModel):
    id: int
    product_id: int
    quantity: int
    address: str


# In-memory stores for example purposes
PRODUCTS = [
    Product(id=1, name="K-Health Tea", price=10.99, description="Korean herbal tea"),
    Product(id=2, name="Ginseng Drink", price=15.49, description="Energy booster"),
    Product(id=3, name="Seaweed Chips", price=4.99, description="Healthy seaweed snack"),
    Product(id=4, name="Kimchi Pack", price=8.25, description="Traditional fermented cabbage"),
    Product(id=5, name="Red Ginseng Candy", price=6.00, description="Sweet immune booster"),
]

ORDERS: List[Order] = []


@app.get("/products", response_model=List[Product])
def list_products() -> List[Product]:
    """Return the list of available health food products."""
    return PRODUCTS


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int) -> Product:
    """Retrieve a product by its ID."""
    for product in PRODUCTS:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/orders", response_model=Order)
def create_order(order: Order) -> Order:
    """Create a new order for a product."""
    if not any(p.id == order.product_id for p in PRODUCTS):
        raise HTTPException(status_code=404, detail="Product not found")
    ORDERS.append(order)
    return order


@app.get("/orders", response_model=List[Order])
def list_orders() -> List[Order]:
    """List all placed orders."""
    return ORDERS


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
