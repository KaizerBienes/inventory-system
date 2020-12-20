from flask import Blueprint, request, Response, json
from flask_api import status
from flask_cors import cross_origin
from inventory.controllers.inventory_controller import InventoryController

DEFAULT_MIMETYPE = 'application/json'


api = Blueprint("api", __name__)

inventory_controller = InventoryController()

@api.route('/inventory/<id>', methods=['GET'])
@cross_origin()
def get_inventory(id: int):
    return inventory_controller.handle_all_errors(
        function_call=inventory_controller.get_inventory,
        request=request,
        params={"inventory_id": id})

@api.route('/inventory', methods=['GET'])
@cross_origin()
def search_inventory():
    return inventory_controller.handle_all_errors(
        function_call=inventory_controller.search_from_key_term,
        request=request,
        params=None)

@api.route('/inventory', methods=['POST'])
@cross_origin()
def create_inventory():
    return inventory_controller.handle_all_errors(
        function_call=inventory_controller.create_inventory,
        request=request,
        params=None)

@api.route('/inventory/<id>', methods=['PUT'])
@cross_origin()
def update_inventory(id: int):
    return inventory_controller.handle_all_errors(
        function_call=inventory_controller.update_inventory,
        request=request,
        params={"inventory_id": id})

@api.route('/inventory/<id>', methods=['DELETE'])
@cross_origin()
def delete_inventory(id: int):
    return inventory_controller.handle_all_errors(
        function_call=inventory_controller.delete_inventory,
        request=request,
        params={"inventory_id": id})