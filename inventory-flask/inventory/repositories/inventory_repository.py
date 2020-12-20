from inventory.models.database import db
from inventory.models.inventory import Inventory, Category, ItemDetail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

class CategoryRepository:
    """
    Manipulates category-related models

    ...

    Attributes
    ----------
    db: SQLAlchemy
        contains our SQLite connection

    Methods
    -------
    get_by_id(self, id)
        Retrieves the category id
    get_by_category_name(self, category_name)
        Retrieves a category record from the given name
    create(self, category_name)
        Creates a category record if it does not exist yet; otherwise, return the existing one
    """

    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_by_id(self, id: int):
        return Category.query.get(id=id)

    def get_by_category_name(self, category_name: str):
        return Category.query.filter_by(name=category_name).first()

    def create(self, category_name: str):
        category = self.get_by_category_name(category_name)
        if not category:
            category = Category(name=category_name)
            self.db.session.add(category)
            self.db.session.flush()

        return category

class InventoryRepository:
    """
    Manipulates inventory-related models

    ...

    Attributes
    ----------
    db: SQLAlchemy
        contains our SQLite connection

    Methods
    -------
    get_by_id(self, id)
        Retrieves the inventory id
    get_by_item_number(self, item_number, inventory_id)
        Retrieves an inventory from the given item number
    create(self, data)
        Creates an inventory entry
    update(self, id, data)
        Updates the provided inventory id
    get_inventory_data_as_dict(self, inventory)
        Converts the given inventory into a dictionary which includes its relationships
    search_from_key_term(self, search_key)
        Retrieves inventories based from the search term
    """

    def __init__(self, db: SQLAlchemy):
        self.db = db
    
    def get_by_id(self, id: int):
        return Inventory.query.get(id)

    def get_by_item_number(self, item_number, inventory_id=None):
        queries = [Inventory.item_number == item_number]
        if inventory_id:
            queries.append(Inventory.id != inventory_id)

        return Inventory.query.filter(*queries).first()

    def create(self, data: dict):
        if self.get_by_item_number(data.get('item_number')):
            raise ValueError('An item with this item number already exists.')

        inventory = Inventory(
            item_number=data.get('item_number'),
            cost_price=data.get('cost_price'),
            quantity=data.get('quantity'),
            unit_abbreviation=data.get('unit_abbreviation'),
            category_id=data.get('category_id'))
        self.db.session.add(inventory)
        self.db.session.flush()
    
        return inventory
    
    def update(self, id: int, data: dict):
        if self.get_by_item_number(item_number=data.get('item_number'), inventory_id=id):
            raise ValueError('An item with this item number already exists.')

        inventory = self.db.session.query(Inventory)\
            .filter(Inventory.id == id)\
            .update({
                'item_number': data.get('item_number'),
                'cost_price': data.get('cost_price'),
                'quantity': data.get('quantity'),
                'unit_abbreviation': data.get('unit_abbreviation'),
                'category_id': data.get('category_id')
            })
        
        return inventory

    def get_inventory_data_as_dict(self, inventory: Inventory):
        get_data = self.db.session\
            .query(
                Category.id.label('category_id'),
                Category.name.label('category_name'),
                Inventory.id.label('inventory_id'),
                Inventory.item_number,
                Inventory.cost_price,
                Inventory.quantity,
                Inventory.unit_abbreviation,
                ItemDetail.id.label('item_detail_id'),
                ItemDetail.item_name,
                ItemDetail.description
            )\
            .join(Category, Category.id == Inventory.category_id)\
            .join(ItemDetail, ItemDetail.inventory_id == Inventory.id)\
            .filter(Inventory.id == inventory.id).first()

        return get_data._asdict() if get_data else None

    def search_from_key_term(self, search_key: str):
        search_filter = True # search all
        if search_key:
            search_filter = or_(Category.name.like("%{}%".format(search_key)),
                    Inventory.item_number.like("%{}%".format(search_key)),
                    ItemDetail.item_name.like("%{}%".format(search_key)))

        search_results = self.db.session\
            .query(
                Category.id.label('category_id'),
                Category.name.label('category_name'),
                Inventory.id.label('inventory_id'),
                Inventory.item_number,
                Inventory.cost_price,
                Inventory.quantity,
                Inventory.unit_abbreviation,
                ItemDetail.id.label('item_detail_id'),
                ItemDetail.item_name,
                ItemDetail.description
            )\
            .join(Category, Category.id == Inventory.category_id)\
            .join(ItemDetail, ItemDetail.inventory_id == Inventory.id)\
            .filter(search_filter).all()

        return [result._asdict() for result in search_results]

class ItemDetailRepository:
    """
    Manipulates item detail-related models

    ...

    Attributes
    ----------
    db: SQLAlchemy
        contains our SQLite connection

    Methods
    -------
    get_by_inventory_id(self, inventory_id)
        Retrieves the item details of the given inventory id
    create(self, inventory_id, item_name, description)
        Creates an item detail from the given inventory id
    update(self, inventory_id, data)
        Updates the provided inventory id item details
    """

    def __init__(self, db):
        self.db = db

    def get_by_inventory_id(self, inventory_id: int):
        return ItemDetail.query.get(inventory_id)

    def create(self, inventory_id: int, item_name: str, description: str):
        item_detail = self.get_by_inventory_id(inventory_id)

        if not item_detail:
            item_detail = ItemDetail(
                inventory_id=inventory_id,
                item_name=item_name,
                description=description)
            self.db.session.add(item_detail)
            self.db.session.flush()

        return item_detail

    def update(self, inventory_id: int, data: dict):
        item_detail = self.db.session.query(ItemDetail)\
            .filter(ItemDetail.inventory_id == inventory_id)\
            .update({
                'item_name': data.get('item_name'),
                'description': data.get('description')
            })

        return item_detail
