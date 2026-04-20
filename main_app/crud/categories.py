from sqlalchemy.orm import Session
from models import Category
from schemas.categories import CategoryCreate, CategoryUpdate


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(db: Session):
    return db.query(Category).all()


def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def update_category(db: Session, category_id: int, update_data: CategoryUpdate):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        return None

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        return None

    db.delete(category)
    db.commit()
    return category
