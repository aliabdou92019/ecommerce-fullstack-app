from sqlalchemy.orm import Session
from models import Product, Category
from schemas.products import ProductCreate,ProductUpdate


def create_product(db: Session, product_data: ProductCreate):
    category = db.query(Category).filter(Category.id == product_data.category_id).first()

    if not category:
        return None

    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        category_id=product_data.category_id
        
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

def get_all_products(db: Session):
    return db.query(Product).all()

def search_products_by_name(db: Session, name: str):
    return db.query(Product).filter(Product.name.contains(name)).all()

def get_in_stock_products(db: Session):
    return db.query(Product).filter(Product.stock > 0).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return None

    update_data = product_data.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        category = db.query(Category).filter(Category.id == update_data["category_id"]).first()
        if not category:
            return "invalid_category"

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return None

    db.delete(product)
    db.commit()
    return product