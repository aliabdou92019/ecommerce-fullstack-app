from models import Order, OrderItem,Product
from schemas.orders import OrderCreate
from sqlalchemy.orm import Session

def add_order(db:Session,order_data:OrderCreate):
  total_price = 0
  order_list = []

  ## add order to order list to get the ID for the order items
  new_order = Order(user_id= order_data.user_id,total_price = total_price)
  db.add(new_order)
  db.flush()  

  for item in order_data.items:
    product = db.query(Product).filter(Product.id == item.product_id).first()
    total_price += product.price*item.quantity
    order_item = OrderItem(
      order_id= new_order.id,
      product_id= product.id,
      quantity=item.quantity,
      price_at_time_of_purchase= product.price
    )
    order_list.append(order_item)
    product.stock = product.stock - order_item.quantity
    
  ## adding the list to database
  new_order.total_price = total_price
  db.add_all(order_list)
  db.commit()
  db.refresh(new_order)
  return new_order

def get_user_orders(user_id:int,db:Session): 
  orders = db.query(Order).filter(Order.user_id == user_id).all()
  return orders

def get_all_orders(user_id: int,db:Session):
  all_orders = db.query(Order)
  return all_orders


def cancel_order(db: Session, order_id: int, user_id: int = None):
    query = db.query(Order).filter(Order.id == order_id)
    
    if user_id:
      query = query.filter(Order.user_id == user_id)
        
    order = query.first()
    
    if not order:
      return False
        
    db.delete(order)
    db.commit()
    return True