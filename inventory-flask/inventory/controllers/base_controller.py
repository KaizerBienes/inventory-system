from flask_api import status
from flask import Response, json
from inventory.responses.inventory_response import InventoryResponse

DEFAULT_MIMETYPE = 'application/json'


class BaseController:
    """
    The base class of all controllers

    ...

    Attributes
    ----------
    request : request
        The request object from flask; contains the payload and query string

    Methods
    -------
    handle_all_errors(function_call, request, params)
        Generic catch all to handle responses from controllers
    """

    def handle_all_errors(self, function_call, request, params):
        """
        Parameters
        ----------
        function_call: func
            A passed controller function from the route
        request: request
            The flask request from the route
        params: dict
            Contains path parameters
        """
        try:
            return function_call(request, params)
        except ValueError as e:
            response_status = status.HTTP_400_BAD_REQUEST
            return Response(
                response=json.dumps(InventoryResponse.generic_error(str(e), response_status)),
                status=response_status,
                mimetype=DEFAULT_MIMETYPE)
        except Exception as e:
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(
                response=json.dumps(InventoryResponse.generic_error(str(e), response_status)),
                status=response_status,
                mimetype=DEFAULT_MIMETYPE)