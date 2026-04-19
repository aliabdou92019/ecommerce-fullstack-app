from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session 

from database import get_db
# from schemas.products import ProductCreate, ProductResponse , ProductDeleteResponse , ProductUpdate
from schemas.products import *
# from crud.products import create_product, get_product_by_id , get_all_products , delete_product, update_product 
from crud.products import * 

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = create_product(db, product)

    if not new_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist"
        )

    return new_product

@router.get("/in-stock", response_model=list[ProductResponse])
def read_in_stock_products(db: Session = Depends(get_db)):
    return get_in_stock_products(db)

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

@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def edit_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(require_admin)        #if User.role != "admin" raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update products")
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
    # current_user: User = Depends(require_admin)   #if User.role != "admin" raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete products")
):
    product = delete_product(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return ProductDeleteResponse(
        message="Product deleted successfully",
        # deleted_by=current_user.username
        deleted_product=product
    )
    
