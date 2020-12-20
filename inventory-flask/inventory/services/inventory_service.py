from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.datastructures import MultiDict

from inventory.models.database import db
from inventory.repositories.inventory_repository import CategoryRepository, InventoryRepository, ItemDetailRepository


class InventoryService:
    """
    Contains the main logic for handling inventory services; manipulates repositories for querying against our models

    ...

    Attributes
    ----------
    db: SQLAlchemy
        contains our SQLite connection
    categoryRepository: CategoryRepository
        handles all category-related model manipulations
    itemDetailRepository: ItemDetailRepository
        handles all item detail-related model manipulations
    inventoryRepository: InventoryRepository
        handles all inventory-related model manipulations

    Methods
    -------
    create_inventory(data)
        Creates the record for the inventory; only creates the category if it does not exist yet
    search_from_key_term(request, search_key)
        Looks for the key term from the inventory list
    get_inventory_by_id(self, id)
        Retrieves a specific inventory given the id
    update_inventory(self, inventory_id, data)
        Updates a given inventory id from the payload provided
    delete_inventory(self, inventory_id)
        deletes the inventory and item detail from the database
    """

    def __init__(self):
        self.db = db
        self.categoryRepository = CategoryRepository(db)
        self.itemDetailRepository = ItemDetailRepository(db)
        self.inventoryRepository = InventoryRepository(db)

    def create_inventory(self, data: MultiDict):
        inventory = None
        try:
            category = self.categoryRepository.create(category_name=data.get('category_name'))
            inventory = self.inventoryRepository.create(data={
                'item_number': data.get('item_number'),
                'cost_price': data.get('cost_price'),
                'quantity': data.get('quantity'),
                'unit_abbreviation': data.get('unit_abbreviation'),
                'category_id': category.id
            })

            item_detail = self.itemDetailRepository.create(
                inventory_id=inventory.id,
                item_name=data.get('item_name'),
                description=data.get('description')
            )

            self.db.session.commit()
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise
        except Exception as e:
            self.db.session.rollback()
            raise

        return self.inventoryRepository.get_inventory_data_as_dict(inventory)

    def search_from_key_term(self, search_key: str):
        return self.inventoryRepository.search_from_key_term(search_key)

    def get_inventory_by_id(self, id: str):
        inventory = self.inventoryRepository.get_by_id(id=id)
        if inventory:
            return self.inventoryRepository.get_inventory_data_as_dict(inventory)
        else:
            raise ValueError("Could not find inventory id.")


    def update_inventory(self, inventory_id: int, data: dict):
        inventory = None
        try:
            inventory = self.get_inventory_by_id(inventory_id)
            category = self.categoryRepository.create(category_name=data.get('category_name'))
            self.inventoryRepository.update(
                id=inventory_id,
                data={
                    'item_number': data.get('item_number'),
                    'cost_price': data.get('cost_price'),
                    'quantity': data.get('quantity'),
                    'unit_abbreviation': data.get('unit_abbreviation'),
                    'category_id': category.id
                })

            item_detail = self.itemDetailRepository.update(
                inventory_id=inventory_id,
                data={
                    'item_name': data.get('item_name'),
                    'description': data.get('description')
                })

            self.db.session.commit()
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise
        except:
            self.db.session.rollback()
            raise

        return self.get_inventory_by_id(inventory_id)

    def delete_inventory(self, inventory_id: str):
        try:
            inventory = self.inventoryRepository.get_by_id(inventory_id)
            if inventory:
                item_detail = self.itemDetailRepository.get_by_inventory_id(inventory_id)
                if item_detail:
                    self.db.session.delete(item_detail)
                    self.db.session.delete(inventory)
                else:
                    raise RuntimeError('Could not find item detail')
                self.db.session.commit()
            else:
                return False
        except SQLAlchemyError as e:
            self.db.session.rollback()
            return None
        except:
            self.db.session.rollback()
            return None
        
        return True