from inventory.models.database import db
from sqlalchemy.sql import func
from datetime import datetime

class Category(db.Model):
    """
    The category model
    Contains categories to group inventories together

    ...

    Attributes
    ----------
    id: 
        the primary key
    name:
        contains the name of the category
    created_at:
        creation date
    updated_at:
        automatically updates when the record is updated
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class Inventory(db.Model):
    """
    The inventory model
    Contains information about the inventory itself

    ...

    Attributes
    ----------
    id: 
        the primary key
    item_number:
        unique identifier for the item; string so that prefixes can be appended e.g. ITEM-001
    cost_price:
        price of the inventory
    quantity:
        number of inventory items on hand; numeric to allow decimals for weights / lengths e.g. 10.255 kg of corn
    unit_abbreviation:
        the unit of the item
    category_id:
        references category.id
    created_at:
        date of when the record was created; defaults to current time
    updated_at:
        date of when the record was last updated; defaults to current time
        
    """
    id = db.Column(db.Integer, primary_key=True)
    item_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    cost_price = db.Column(db.Numeric(27, 8), nullable=False)
    quantity = db.Column(db.Numeric(27, 8), nullable=False)
    unit_abbreviation = db.Column(db.String(10), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class ItemDetail(db.Model):
    """
    The item detail model
    Contains details, usually display-related, about the inventory item

    ...

    Attributes
    ----------
    id: 
        the primary key
    inventory_id:
        references inventory.id
    item_name:
        a non-unique item name of the inventory
    description:
        a description of the inventory item
    created_at:
        date of when the record was created; defaults to current time
    updated_at:
        date of when the record was last updated; defaults to current time
        
    """
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    item_name = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())