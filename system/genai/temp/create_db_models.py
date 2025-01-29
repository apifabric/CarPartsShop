# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from decimal import Decimal
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Part(Base):
    """description: Model for individual car parts available in the shop."""
    __tablename__ = 'part'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    price = Column(Integer)
    stock_quantity = Column(Integer)

class Supplier(Base):
    """description: Model for suppliers providing car parts to the shop."""
    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    contact_number = Column(String)
    address = Column(String)

class Category(Base):
    """description: Model for different categories of car parts."""
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

class PartCategory(Base):
    """description: Junction table to establish many-to-many relationship between parts and categories."""
    __tablename__ = 'part_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    part_id = Column(Integer, ForeignKey('part.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

class Customer(Base):
    """description: Model representing customers purchasing car parts."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

class Order(Base):
    """description: Model representing each order made by customers."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    date = Column(Date)

class OrderItem(Base):
    """description: Model for individual items within an order, linking orders with parts."""
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    part_id = Column(Integer, ForeignKey('part.id'))
    quantity = Column(Integer)

class Employee(Base):
    """description: Model for shop employees."""
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    hire_date = Column(Date)
    position = Column(String)

class Inventory(Base):
    """description: Model representing inventory details for parts."""
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String)
    part_id = Column(Integer, ForeignKey('part.id'))
    quantity = Column(Integer)

class SupplierOrder(Base):
    """description: Model representing orders made to suppliers."""
    __tablename__ = 'supplier_order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    date = Column(Date)

class SupplierOrderItem(Base):
    """description: Model for items within a supplier order, linking Supplier Orders with Parts."""
    __tablename__ = 'supplier_order_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_order_id = Column(Integer, ForeignKey('supplier_order.id'))
    part_id = Column(Integer, ForeignKey('part.id'))
    quantity = Column(Integer)

class Warranty(Base):
    """description: Model representing warranty information associated with parts."""
    __tablename__ = 'warranty'
    id = Column(Integer, primary_key=True, autoincrement=True)
    part_id = Column(Integer, ForeignKey('part.id'))
    expiration_date = Column(Date)


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    part_row_1 = Part(name="Brake Pad", supplier_id=1, price=50, stock_quantity=100)
    part_row_2 = Part(name="Oil Filter", supplier_id=2, price=30, stock_quantity=150)
    part_row_3 = Part(name="Air Filter", supplier_id=3, price=40, stock_quantity=200)
    part_row_4 = Part(name="Battery", supplier_id=4, price=200, stock_quantity=60)
    supplier_row_1 = Supplier(name="ACME Parts", contact_number="1234567890", address="123 Main St")
    supplier_row_2 = Supplier(name="Auto Supplies Co.", contact_number="0987654321", address="456 Park Ave")
    supplier_row_3 = Supplier(name="SpareParts Warehouse", contact_number="3216549870", address="789 Elm Rd")
    supplier_row_4 = Supplier(name="Parts Hub", contact_number="6549873210", address="101 Pine St")
    category_row_1 = Category(name="Electrical")
    category_row_2 = Category(name="Brakes")
    category_row_3 = Category(name="Filters")
    category_row_4 = Category(name="Batteries")
    
    
    
    session.add_all([part_row_1, part_row_2, part_row_3, part_row_4, supplier_row_1, supplier_row_2, supplier_row_3, supplier_row_4, category_row_1, category_row_2, category_row_3, category_row_4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
