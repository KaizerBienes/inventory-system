from werkzeug.datastructures import MultiDict
from flask_api import status
from flask import Response
import simplejson as json

from inventory.validators.inventory_validator\
    import CreateInventoryValidator, GetInventoryValidator, SearchInventoryValidator,\
    DeleteInventoryValidator, UpdateInventoryValidator
from inventory.services.inventory_service import InventoryService
from inventory.responses.inventory_response import InventoryResponse
from inventory.controllers.base_controller import BaseController

DEFAULT_MIMETYPE = 'application/json'

class InventoryController(BaseController):
    """
    A class which orchestrates inventory's validation, passing to services and responding to routes

    ...

    Attributes
    ----------
    inventory_service : InventoryService
        the service that handles the actual logic for manipulating entries

    Methods
    -------
    create_inventory(request, params)
        creates the inventory
    """

    def __init__(self):
        self.inventory_service = InventoryService()

    def create_inventory(self, request, params):
        form = CreateInventoryValidator(request.form)
        if form.validate():
            return Response(
                response=json.dumps(InventoryResponse.format_inventory(self.inventory_service.create_inventory(request.form))),
                status=status.HTTP_200_OK,
                mimetype=DEFAULT_MIMETYPE)
        else:
            return Response(
                response=json.dumps(InventoryResponse.format_validation_errors(form.errors, status.HTTP_406_NOT_ACCEPTABLE)),
                status=status.HTTP_406_NOT_ACCEPTABLE,
                mimetype=DEFAULT_MIMETYPE)
    
    def get_inventory(self, request, params):
        form = GetInventoryValidator(MultiDict({'inventory_id': params.get('inventory_id')}))
        if form.validate():
            return Response(
                response=json.dumps(InventoryResponse.format_inventory(self.inventory_service.get_inventory_by_id(params.get('inventory_id')))),
                status=status.HTTP_200_OK,
                mimetype=DEFAULT_MIMETYPE)
        else:
            return Response(
                response=json.dumps(InventoryResponse.format_validation_errors(form.errors, status.HTTP_406_NOT_ACCEPTABLE)),
                status=status.HTTP_406_NOT_ACCEPTABLE,
                mimetype=DEFAULT_MIMETYPE)

    def update_inventory(self, request, params):
        form = UpdateInventoryValidator(request.form)
        if form.validate():
            return Response(
                response=json.dumps(InventoryResponse.format_inventory(
                    self.inventory_service.update_inventory(
                        params.get('inventory_id'),
                        request.form))),
                status=status.HTTP_200_OK,
                mimetype=DEFAULT_MIMETYPE)
        else:
            return Response(
                response=json.dumps(InventoryResponse.format_validation_errors(form.errors, status.HTTP_406_NOT_ACCEPTABLE)),
                status=status.HTTP_406_NOT_ACCEPTABLE,
                mimetype=DEFAULT_MIMETYPE)

    def delete_inventory(self, request, params):
        form = GetInventoryValidator(MultiDict({'inventory_id': params.get('inventory_id')}))
        if form.validate():
            deleted = self.inventory_service.delete_inventory(params.get('inventory_id'))
            if deleted:
                return Response(
                    response=json.dumps(InventoryResponse.generic_message('Deleted successfully.', status.HTTP_200_OK)),
                    status=status.HTTP_200_OK,
                    mimetype=DEFAULT_MIMETYPE)
            else:
                raise ValueError('Could not find inventory entry.')
        else:
            return Response(
                response=json.dumps(InventoryResponse.format_validation_errors(form.errors, status.HTTP_406_NOT_ACCEPTABLE)),
                status=status.HTTP_406_NOT_ACCEPTABLE,
                mimetype=DEFAULT_MIMETYPE)

    def search_from_key_term(self, request, params):
        """
        Parameters
        ----------
        request: request
            The flask request from the route
        params: dict
            Contains path parameters for the search term
        """
        form = SearchInventoryValidator(request.args)
        if form.validate():
            return Response(
                response=json.dumps(InventoryResponse.format_inventories(
                    self.inventory_service.search_from_key_term(request.args.get('search')))),
                status=status.HTTP_200_OK,
                mimetype=DEFAULT_MIMETYPE)
        else:
            return Response(
                response=json.dumps(InventoryResponse.format_validation_errors(form.errors, status.HTTP_406_NOT_ACCEPTABLE)),
                status=status.HTTP_406_NOT_ACCEPTABLE,
                mimetype=DEFAULT_MIMETYPE)
