from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session 

from database import get_db
from schemas.products import *
from crud.products import * 
from dependencies import *
from models import *

router = APIRouter(prefix="/products", tags=["Products"])


# Admin only: create product
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    new_product = create_product(db, product)

    if new_product == "invalid_category":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist"
        )

    if new_product == "duplicate_product":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product already exists in this category"
        )

    return new_product

@router.get(
    "/in-stock",
    response_model=list[ProductResponse],
    response_model_exclude_none=True
)
def read_in_stock_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    products = get_in_stock_products(db)

    result = []

    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id,
        }

        if current_user.role == "admin" or product.stock <= 3:
            product_data["stock"] = product.stock

        result.append(product_data)

    return result

@router.get("/", response_model=list[ProductResponse])
def read_products(db: Session = Depends(get_db)):
    return get_all_products(db)

@router.get("/search", response_model=list[ProductResponse])
def search_products(
    name: str = Query(..., min_length=1, description="Search by product name"),
    db: Session = Depends(get_db)
):
    return search_products_by_name(db, name)

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product

@router.get("/category/{category_id}", response_model=list[ProductResponse])
def read_products_by_category(category_id: int, db: Session = Depends(get_db)):
    return get_products_by_category(db, category_id)

@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def edit_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    updated_product = update_product(db, product_id, product_data)

    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if updated_product == "invalid_category":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist"
        )

    return updated_product

@router.delete("/{product_id}", response_model=ProductDeleteResponse, status_code=status.HTTP_200_OK)
def remove_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    product = delete_product(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return ProductDeleteResponse(
        message="Product deleted successfully",
        deleted_product=product
    )
    
