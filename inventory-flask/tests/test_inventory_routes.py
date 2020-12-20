import pytest

from flask_api import status
from inventory import create_app
from inventory.models.database import db
from inventory.models.inventory import Category, Inventory, ItemDetail

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.testing = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

    client = app.test_client()
    with app.app_context():
        db.create_all()
        category = Category(id=1, name='stub_category')
        inventory = Inventory(id=1, category_id=1, item_number='stub_item_number',
            cost_price=1, quantity=1, unit_abbreviation='stub_unit')
        item_detail = ItemDetail(id=1, inventory_id=1, item_name='stub_item_name',
            description='stub_description')

        second_inventory = Inventory(id=2, category_id=1, item_number='stub_item_number_2',
            cost_price=2, quantity=2, unit_abbreviation='stub_unit_2')
        second_item_detail = ItemDetail(id=2, inventory_id=2, item_name='stub_item_name_2',
            description='stub_description_2')

        db.session.add(category)
        db.session.add(inventory)
        db.session.add(item_detail)
        db.session.add(second_inventory)
        db.session.add(second_item_detail)
        db.session.commit()
    yield client

def test_get_inventory(client):
    rv = client.get("/api/inventory/1")
    assert(rv.json == {
        'data': {
            'category': {
                'id': 1,
                'name': 'stub_category'
            },
            'inventory': {
                'id': 1,
                'cost_price': 1,
                'item_number': 'stub_item_number',
                'quantity': 1,
                'unit_abbreviation': 'stub_unit'
            },
            'item_detail': {
                'id': 1,
                'item_name': 'stub_item_name',
                'description': 'stub_description'
            }
        }
    })

def test_get_unknown_inventory(client):
    rv = client.get("/api/inventory/unknown_inventory_id")
    assert(rv.json['error']['code'] == status.HTTP_406_NOT_ACCEPTABLE)
    assert(rv.json['error']['message'] == 'Validation errors')
    assert(rv.json['error']['errors'] == {
        'inventory_id': ['Not a valid integer value']
    })

def test_get_inventories(client):
    rv = client.get("/api/inventory")
    assert(rv.json == {
        'data': [
            {
                'category': {
                    'id': 1,
                    'name': 'stub_category'
                },
                'inventory': {
                    'id': 1,
                    'cost_price': 1,
                    'item_number': 'stub_item_number',
                    'quantity': 1,
                    'unit_abbreviation': 'stub_unit'
                },
                'item_detail': {
                    'id': 1,
                    'item_name': 'stub_item_name',
                    'description': 'stub_description'
                }
            },
            {
                'category': {
                    'id': 1,
                    'name': 'stub_category'
                },
                'inventory': {
                    'id': 2,
                    'cost_price': 2,
                    'item_number': 'stub_item_number_2',
                    'quantity': 2,
                    'unit_abbreviation': 'stub_unit_2'
                },
                'item_detail': {
                    'id': 2,
                    'item_name': 'stub_item_name_2',
                    'description': 'stub_description_2'
                }
            }
        ]
    })

def test_create_inventory(client):
    rv = client.post("/api/inventory", data={
        'category_name': 'stub_category',
        'cost_price': 1,
        'item_name': 'stub_create_item_name',
        'item_number': 'stub_create_item_number',
        'quantity': 1,
        'unit_abbreviation': 'stub_unit',
        'description': 'stub_description'
    })

    assert(rv.json['data']['category']['name'] == 'stub_category')
    assert(rv.json['data']['inventory']['cost_price'] == 1)
    assert(rv.json['data']['inventory']['item_number'] == 'stub_create_item_number')
    assert(rv.json['data']['inventory']['quantity'] == 1)
    assert(rv.json['data']['inventory']['unit_abbreviation'] == 'stub_unit')
    assert(rv.json['data']['item_detail']['item_name'] == 'stub_create_item_name')
    assert(rv.json['data']['item_detail']['description'] == 'stub_description')

def test_invalid_duplicate_item_number(client):
    rv = client.post("/api/inventory", data={
        'category_name': 'stub_category',
        'cost_price': 1,
        'item_name': 'stub_item_name_test',
        'item_number': 'stub_item_number',
        'quantity': 1,
        'unit_abbreviation': 'stub_unit',
        'description': 'stub_description'
    })

    assert(rv.json['error']['code'] == status.HTTP_400_BAD_REQUEST)
    assert(rv.json['error']['message'] == 'An item with this item number already exists.')

def test_invalid_cost_price(client):
    rv = client.post("/api/inventory", data={
        'category_name': 'stub_category',
        'cost_price': -1,
        'item_name': 'stub_item_name',
        'item_number': 'stub_item_number_test',
        'quantity': 1,
        'unit_abbreviation': 'stub_unit',
        'description': 'stub_description'
    })

    assert(rv.json['error']['code'] == status.HTTP_406_NOT_ACCEPTABLE)
    assert(rv.json['error']['message'] == 'Validation errors')
    assert(rv.json['error']['errors'] == {
        'cost_price': ['Number must be between 0 and 1000000.']
    })

def test_invalid_quantity(client):
    rv = client.post("/api/inventory", data={
        'category_name': 'stub_category',
        'cost_price': 1,
        'item_name': 'stub_item_name',
        'item_number': 'stub_item_number_test',
        'quantity': -1,
        'unit_abbreviation': 'stub_unit',
        'description': 'stub_description'
    })

    assert(rv.json['error']['code'] == status.HTTP_406_NOT_ACCEPTABLE)
    assert(rv.json['error']['message'] == 'Validation errors')
    assert(rv.json['error']['errors'] == {
        'quantity': ['Number must be between 0 and 10000000.']
    })

def test_delete_inventory_item(client):
    rv = client.delete("/api/inventory/1")
    assert(rv.json['error']['code'] == status.HTTP_200_OK)
    assert(rv.json['error']['message'] == 'Deleted successfully.')

def test_delete_unknown_inventory_id(client):
    rv = client.delete("/api/inventory/unknown_inventory_id")
    assert(rv.json['error']['code'] == status.HTTP_406_NOT_ACCEPTABLE)
    assert(rv.json['error']['message'] == 'Validation errors')
    assert(rv.json['error']['errors'] == {
        'inventory_id': ['Not a valid integer value']
    })

def test_update_inventory(client):
    rv = client.put("/api/inventory/1", data={
        'inventory_id': 1,
        'category_name': 'updated_stub_category',
        'cost_price': 1,
        'item_name': 'updated_stub_item_name',
        'item_number': 'updated_stub_item_number',
        'quantity': 1,
        'unit_abbreviation': 'stub_unit',
        'description': 'updated_stub_description'
    })

    assert(rv.json['data']['category']['name'] == 'updated_stub_category')
    assert(rv.json['data']['inventory']['cost_price'] == 1)
    assert(rv.json['data']['inventory']['item_number'] == 'updated_stub_item_number')
    assert(rv.json['data']['inventory']['quantity'] == 1)
    assert(rv.json['data']['inventory']['unit_abbreviation'] == 'stub_unit')
    assert(rv.json['data']['item_detail']['item_name'] == 'updated_stub_item_name')
    assert(rv.json['data']['item_detail']['description'] == 'updated_stub_description')