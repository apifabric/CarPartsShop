# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  January 29, 2025 08:03:37
# Database: sqlite:////tmp/tmp.V7mKLyWZ4a-01JJRHBREBNYSRXAD5QA1YX00T/CarPartsShop/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX, TestBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy, os
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

if os.getenv('APILOGICPROJECT_NO_FLASK') is None or os.getenv('APILOGICPROJECT_NO_FLASK') == 'None':
    Base = SAFRSBaseX   # enables rules to be used outside of Flask, e.g., test data loading
else:
    Base = TestBase     # ensure proper types, so rules work for data loading
    print('*** Models.py Using TestBase ***')



class Category(Base):  # type: ignore
    """
    description: Model for different categories of car parts.
    """
    __tablename__ = 'category'
    _s_collection_name = 'Category'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    PartCategoryList : Mapped[List["PartCategory"]] = relationship(back_populates="category")



class Customer(Base):  # type: ignore
    """
    description: Model representing customers purchasing car parts.
    """
    __tablename__ = 'customer'
    _s_collection_name = 'Customer'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")



class Employee(Base):  # type: ignore
    """
    description: Model for shop employees.
    """
    __tablename__ = 'employee'
    _s_collection_name = 'Employee'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hire_date = Column(Date)
    position = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)



class Supplier(Base):  # type: ignore
    """
    description: Model for suppliers providing car parts to the shop.
    """
    __tablename__ = 'supplier'
    _s_collection_name = 'Supplier'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_number = Column(String)
    address = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    PartList : Mapped[List["Part"]] = relationship(back_populates="supplier")
    SupplierOrderList : Mapped[List["SupplierOrder"]] = relationship(back_populates="supplier")



class Order(Base):  # type: ignore
    """
    description: Model representing each order made by customers.
    """
    __tablename__ = 'order'
    _s_collection_name = 'Order'  # type: ignore

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'))
    date = Column(Date)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="order")



class Part(Base):  # type: ignore
    """
    description: Model for individual car parts available in the shop.
    """
    __tablename__ = 'part'
    _s_collection_name = 'Part'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    supplier_id = Column(ForeignKey('supplier.id'))
    price = Column(Integer)
    stock_quantity = Column(Integer)

    # parent relationships (access parent)
    supplier : Mapped["Supplier"] = relationship(back_populates=("PartList"))

    # child relationships (access children)
    InventoryList : Mapped[List["Inventory"]] = relationship(back_populates="part")
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="part")
    PartCategoryList : Mapped[List["PartCategory"]] = relationship(back_populates="part")
    SupplierOrderItemList : Mapped[List["SupplierOrderItem"]] = relationship(back_populates="part")
    WarrantyList : Mapped[List["Warranty"]] = relationship(back_populates="part")



class SupplierOrder(Base):  # type: ignore
    """
    description: Model representing orders made to suppliers.
    """
    __tablename__ = 'supplier_order'
    _s_collection_name = 'SupplierOrder'  # type: ignore

    id = Column(Integer, primary_key=True)
    supplier_id = Column(ForeignKey('supplier.id'))
    date = Column(Date)

    # parent relationships (access parent)
    supplier : Mapped["Supplier"] = relationship(back_populates=("SupplierOrderList"))

    # child relationships (access children)
    SupplierOrderItemList : Mapped[List["SupplierOrderItem"]] = relationship(back_populates="supplier_order")



class Inventory(Base):  # type: ignore
    """
    description: Model representing inventory details for parts.
    """
    __tablename__ = 'inventory'
    _s_collection_name = 'Inventory'  # type: ignore

    id = Column(Integer, primary_key=True)
    location = Column(String)
    part_id = Column(ForeignKey('part.id'))
    quantity = Column(Integer)

    # parent relationships (access parent)
    part : Mapped["Part"] = relationship(back_populates=("InventoryList"))

    # child relationships (access children)



class OrderItem(Base):  # type: ignore
    """
    description: Model for individual items within an order, linking orders with parts.
    """
    __tablename__ = 'order_item'
    _s_collection_name = 'OrderItem'  # type: ignore

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'))
    part_id = Column(ForeignKey('part.id'))
    quantity = Column(Integer)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderItemList"))
    part : Mapped["Part"] = relationship(back_populates=("OrderItemList"))

    # child relationships (access children)



class PartCategory(Base):  # type: ignore
    """
    description: Junction table to establish many-to-many relationship between parts and categories.
    """
    __tablename__ = 'part_category'
    _s_collection_name = 'PartCategory'  # type: ignore

    id = Column(Integer, primary_key=True)
    part_id = Column(ForeignKey('part.id'))
    category_id = Column(ForeignKey('category.id'))

    # parent relationships (access parent)
    category : Mapped["Category"] = relationship(back_populates=("PartCategoryList"))
    part : Mapped["Part"] = relationship(back_populates=("PartCategoryList"))

    # child relationships (access children)



class SupplierOrderItem(Base):  # type: ignore
    """
    description: Model for items within a supplier order, linking Supplier Orders with Parts.
    """
    __tablename__ = 'supplier_order_item'
    _s_collection_name = 'SupplierOrderItem'  # type: ignore

    id = Column(Integer, primary_key=True)
    supplier_order_id = Column(ForeignKey('supplier_order.id'))
    part_id = Column(ForeignKey('part.id'))
    quantity = Column(Integer)

    # parent relationships (access parent)
    part : Mapped["Part"] = relationship(back_populates=("SupplierOrderItemList"))
    supplier_order : Mapped["SupplierOrder"] = relationship(back_populates=("SupplierOrderItemList"))

    # child relationships (access children)



class Warranty(Base):  # type: ignore
    """
    description: Model representing warranty information associated with parts.
    """
    __tablename__ = 'warranty'
    _s_collection_name = 'Warranty'  # type: ignore

    id = Column(Integer, primary_key=True)
    part_id = Column(ForeignKey('part.id'))
    expiration_date = Column(Date)

    # parent relationships (access parent)
    part : Mapped["Part"] = relationship(back_populates=("WarrantyList"))

    # child relationships (access children)
