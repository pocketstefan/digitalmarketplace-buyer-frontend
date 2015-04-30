from flask import jsonify, current_app

from . import status
from . import utils
from .. import models


@status.route('/_status')
def status():

    api_response = utils.return_response_from_api_status_call(
        models.get_api_status
    )

    search_api_response = utils.return_response_from_api_status_call(
        models.get_search_api_status
    )

    apis_wot_got_errors = []

    if api_response is None or api_response.status_code is not 200:
        apis_wot_got_errors.append("(Data) API")

    if search_api_response is None or search_api_response.status_code is not 200:
        apis_wot_got_errors.append("Search API")

    # if no errors found, return everything
    if not apis_wot_got_errors:
        return jsonify(
            status="ok",
            version=utils.get_version_label(),
            api_status=api_response.json(),
            search_api_status=search_api_response.json(),
        )

    message = "Error connecting to the " \
              + (" and the ".join(apis_wot_got_errors)) \
              + "."

    current_app.logger.error(message)

    return jsonify(
        status="error",
        version=utils.get_version_label(),
        api_status=None if api_response is None else api_response.json(),
        search_api_status=None if search_api_response is None else search_api_response.json(),
        message=message,
    ), 500