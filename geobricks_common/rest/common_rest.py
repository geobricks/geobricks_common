import json
from flask import Blueprint
from flask import Response
from flask import request
from flask.ext.cors import cross_origin
from geobricks_common.config.config import config

from geobricks_common.core import filesystem

app = Blueprint(__name__, __name__)


@app.route('/')
@cross_origin(origins='*')
def root():
    """
    Root REST service.
    @return: Welcome message.
    """
    return 'Welcome to Geobricks Common!'

@app.route('/discovery/')
@cross_origin(origins='*')
def discovery():
    """
    Discovery service available for all Geobricks libraries that describes the plug-in.
    @return: Dictionary containing information about the service.
    """
    out = {
        'name': 'common',
        'title': 'Geobricks Common Service',
        'description': 'Functionalities to handle common methods.',
        'type': 'SERVICE',

    }
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@app.route('/filesystem/storage/<layerName>', methods=['GET'])
@cross_origin(origins='*', headers=['Content-Type'])
def filesystem_storage_layerName(layerName):
    result = filesystem.get_raster_path_storage(layerName)
    return Response(json.dumps({ "path": result}), content_type='application/json; charset=utf-8')


@app.route('/filesystem/geoserver/<workspace>/<layerName>', methods=['GET'])
@cross_origin(origins='*', headers=['Content-Type'])
def filesystem_geoserver_workspace_layerName(workspace, layerName):
    result = filesystem.get_raster_path_published(workspace, layerName)
    return Response(json.dumps({ "path": result}), content_type='application/json; charset=utf-8')