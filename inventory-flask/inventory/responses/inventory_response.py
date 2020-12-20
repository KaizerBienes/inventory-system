from inventory.models.inventory import Inventory

class InventoryResponse:
    """
    Formats the responses from the controller; only contains static calls as we don't need to perform any logic

    ...

    Methods
    -------
    format_inventory(inventory_dict)
        formats a single inventory
    format_inventories(inventory_list)
        formats multiple inventory dictionaries
    generic_format_inventory(inventory_dict)
        extracted duplication for single and multiple entries
    generic_error(error_message, status_code)
        returns response for an unknown error
    generic_message(message, status_code)
        returns response for an expected message
    """

    @staticmethod
    def format_inventory(inventory_dict: dict):
        return {
            'data': InventoryResponse.generic_format_inventory(inventory_dict)
        }

    @staticmethod
    def format_inventories(inventory_list: list):
        return {
            'data': [InventoryResponse.generic_format_inventory(inventory) for inventory in inventory_list]
        }

    @staticmethod
    def generic_format_inventory(inventory_dict: dict):
        return {
            'category': {
                'id': inventory_dict.get('category_id'),
                'name': inventory_dict.get('category_name'),
            },
            'inventory': {
                'id': inventory_dict.get('inventory_id'),
                'item_number': inventory_dict.get('item_number'),
                'cost_price': inventory_dict.get('cost_price'),
                'quantity': inventory_dict.get('quantity'),
                'unit_abbreviation': inventory_dict.get('unit_abbreviation'),
            },
            'item_detail': {
                'id': inventory_dict.get('item_detail_id'),
                'item_name': inventory_dict.get('item_name'),
                'description': inventory_dict.get('description')
            }
        }

    @staticmethod
    def generic_error(error_message: str, status_code: int):
        return {
            'error': {
                'code': status_code,
                'message': error_message
            }
        }

    @staticmethod
    def generic_message(message: str, status_code: int):
        return {
            'error': {
                'code': status_code,
                'message': message
            }
        }
    
    @staticmethod
    def format_validation_errors(errors: list, status_code: int):
        return {
            'error': {
                'code': status_code,
                'message': 'Validation errors',
                'errors': errors
            }
        }