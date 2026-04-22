from fastapi import APIRouter, HTTPException, Depends,status
from sqlalchemy.orm import Session
from database import get_db
from models import *
from schemas.orders import * 
from crud.orders import * 

router = APIRouter(prefix='/api/v1/orders',tags=['Orders'])

@router.post('/create',response_model=OrderResponse,status_code=status.HTTP_201_CREATED)
def create_order(order_data:OrderCreate,db:Session =Depends(get_db)):
  new_order = add_order(db,order_data)
  if not new_order:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, 
      detail="Could not create order. Please check product stock."
    )
  return new_order

@router.get('get/user/{user_id}',response_model=List[OrderResponse])
def read_user_orders(user_id:int,db:Session = Depends(get_db)):
  orders = get_user_orders(user_id,db)
  if not orders:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found for this user")
  return orders

@router.get('/get_all_orders',response_model=List[OrderResponse])
def admin_order_panel(user_id:int,db:Session = Depends(get_db)):
  user = db.query(User).filter(User.id ==user_id).first()
  if user.role != 'admin':
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Admin")
  all_orders = get_all_orders(user_id,db)
  if not all_orders:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No orders found")
  return all_orders

## get_current_role 
@router.delete('/cancel/{order_id}')
def delete_order(user_id: int,order_id:int,db: Session = Depends(get_db)): ##
  user = db.query(User).filter(User.id == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
  
  if user.role == 'admin':
    canceled = cancel_order(db,order_id)
    if not canceled:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    return {'messege':f'order {order_id} has been canceled'}
  else:
    canceled = cancel_order(db,order_id,user_id)
    if not canceled:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    return {'messege':f'order {order_id} has been canceled'}