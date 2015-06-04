import os
import tempfile
import uuid
import zipfile
import shutil
import requests
import json
from geobricks_common.config.config import config
from geobricks_common.core.log import logger


log = logger(__file__)

# temporary folder
try:
    tmp_folder = config["settings"]["folders"]["tmp"]
except Exception, e:
    tmp_folder = tempfile.gettempdir()

try:
    workspace_layer_separator = config["settings"]["folders"]["workspace_layer_separator"]
except Exception, e:
    workspace_layer_separator = ":"


def create_tmp_filename(extension='', filename='',  subfolder='', add_uuid=True, folder_tmp=tmp_folder):
    """
    Create the path for a tmp file and filename
    :param extension: i.e. "tif"
    :param subfolder: "modis_folder"
    :param filename: "modis"
    :param add_uuid: add or not a uuid to the file
    :param folder_tmp: if not specified it takes the default tmp folder of the os.
    :return: a path to a tmp file
    """
    if extension != '' and "." not in extension: extension = "." + extension
    folder_path = os.path.join(folder_tmp, subfolder)
    if subfolder is not '' and subfolder is not None:
        try:
            os.makedirs(folder_path)
        except Exception, e:
            # log.warn(e)
            pass
    file_path = os.path.join(folder_path, filename)
    if add_uuid:
        return (file_path + str(uuid.uuid4()) + extension).encode('utf-8')
    else:
        return (file_path + extension).encode('utf-8')


def zip_files(name, files, path=tmp_folder):
    extension = ".zip"
    if ".zip" in name:
        extension = ""
    zip_path = os.path.join(path, name + extension)
    zf = zipfile.ZipFile(zip_path, "w")
    zip_subdir = path
    for fpath in files:
        fdir, fname = os.path.split(fpath)
        #Add file, at correct path
        zf.write(fpath, fname)
    zf.close()
    return zip_path


# create zip file with subfolders
def createZip(outputFilePath, pathsToZip, archiveType="zip", zipType=zipfile.ZIP_DEFLATED):
    """
    Create a zip file with a list of files or folders
    :param outputFilePath: path to the output zip file (without .zip). If None it creates a tmp zipfile
    :param pathsToZip: array containing the paths of folders to zip
    :param archiveType: "zip" (the only currently supported)
    :param zipType: i.e. zipfile.ZIP_DEFLATED
    :return: the path to the zipped file
    """
    if outputFilePath is None:
        outputFilePath = create_tmp_filename(".zip")
    zipfilename = "%s.%s" % (outputFilePath, archiveType)
    # log.info("zip filename: %s" % zipfilename)
    zfile = zipfile.ZipFile(os.path.join(zipfilename), 'w', zipType)
    for path in pathsToZip:
        # log.info("processing: %s" % path)
        if not os.path.exists(path):
            log.error("ERROR, folder doesn't exists: %s" % path)

        try:
            if os.path.isdir(path):
                # rootlen => zipped files don't have a deep file tree
                rootlen = len(path) + 1
                for base, dirs, files in os.walk(path):
                    for file in files:
                        dirname = os.path.split(path)[1]
                        fn = os.path.join(base, file)
                        zfile.write(fn, os.path.join(dirname, fn[rootlen:]))
            else:
                zfile.write(path, os.path.basename(path))
        except Exception, e:
            print e
            log.error(e)
            pass
    zfile.close()
    return zipfilename

def make_archive(dir_to_zip, output_filename, archive_type='zip'):
    return shutil.make_archive(output_filename, format=archive_type, root_dir=dir_to_zip)


def get_filename(filepath, extension=False):
    drive, path = os.path.splitdrive(filepath)
    path, filename = os.path.split(path)
    name = os.path.splitext(filename)[0]
    if extension is True:
        return path, filename, name
    else:
        return name


def get_file_extension(filepath):
    return os.path.splitext(os.path.basename(filepath))[1].split(".")[1]


def sanitize_name(name):
    """
    This method clean the name of a layer, should be avoided to use dots as names
    :param name: name of the layer
    :return: sanitized layer name
    """
    name = name.replace(".", "")
    name = name.replace(" ", "_")
    name = name.lower()
    return name


### Get Vector Path
def get_vector_path(metadata):
    '''
    :param metadata: JSON metadata returned by D3S or uid
    :return: raster absolute path
    '''
    log.info(metadata)
    if "path" in metadata:
        # TODO: should be here directly or at the end?
        # TODO: check for relative paths?
        return metadata["path"]

    # if dsd is present in the metadata use it, otherwise is already passed the dsd part
    if "dsd" in metadata:
        metadata = metadata["dsd"]

    # if layerName or UID not present the layer cannot be retrieved
    if "layerName" not in metadata and "uid" not in metadata:
        log.error("No layerName set in the metadata JSON")
        return None


    # if layerName is not present the layer cannot be retrieved
    # if "layerName" not in metadata:
    #     log.error("No layerName set in the metadata JSON")
    #     return None


    path = get_vector_by_datasource(metadata)
    if path is None:
        # if nothing else didn't work check with metadata
        if "uid" in metadata:
            path = get_vector_by_datasource(_get_metadata_by_uid(metadata["uid"]))

    metadata_path = metadata["path"] if "path" in metadata else None
    if metadata_path is not None:
        return metadata_path

    return path


def get_vector_by_datasource(metadata):
    workspace = metadata["workspace"] if "workspace" in metadata else None
    layername = metadata["layerName"] if "layerName" in metadata else None
    if "datasource" in metadata:
        # TODO: handle exception better (i.e. postgis and geoserver togheter)
        if "storage" in metadata["datasource"]:
            return get_vector_path_storage(layername)
        elif "geoserver" in metadata["datasource"]:
            msg = "Shapefiles are not handled in Geoserver at the moment. Metadata " + metadata["layerName"] + " not valid."
            raise Exception(msg)
    return None

def get_vector_path_storage(layername, ext=".shp"):
    path = os.path.join(config["settings"]["folders"]["storage"], "vector",  layername, layername + ext)
    if not os.path.isfile(path):
        log.error("File on storage doesn't exists: " + path)
    return path


### Get Raster Path
def get_raster_path(metadata):
    '''
    :param metadata: JSON metadata returned by D3S or uid
    :return: raster absolute path
    '''
    log.info(metadata)
    if "path" in metadata:
        # TODO: should be here directly or at the end?
        # TODO: check for relative paths?
        return metadata["path"]

    # if dsd is present in the metadata use it, otherwise is already passed the dsd part
    if "dsd" in metadata:
        metadata = metadata["dsd"]

    # if layerName or UID not present the layer cannot be retrieved
    if "layerName" not in metadata and "uid" not in metadata:
        log.error("No layerName set in the metadata JSON")
        return None


    # if layerName is not present the layer cannot be retrieved
    # if "layerName" not in metadata:
    #     log.error("No layerName set in the metadata JSON")
    #     return None

    path = get_raster_by_datasource(metadata)
    if path is None:
        # if nothing else didn't work check with metadata
        if "uid" in metadata:
            path = get_raster_by_datasource(_get_metadata_by_uid(metadata["uid"]))
    return path


def get_raster_by_datasource(metadata):
    workspace = metadata["workspace"] if "workspace" in metadata else None
    layername = metadata["layerName"] if "layerName" in metadata else None
    if "datasource" in metadata:
        # TODO: handle exception better (i.e. postgis and geoserver togheter)
        if "storage" in metadata["datasource"]:
            return get_raster_path_storage(layername)
        elif "geoserver" in metadata["datasource"]:
            return get_raster_path_published(workspace, layername)
    return None


def get_raster_path_published(workspace, layername, ext=".geotiff"):
    path = os.path.join(config["settings"]["folders"]["geoserver_datadir"], "data",  workspace, layername, layername + ext)
    if not os.path.isfile(path):
        log.error("File on geoserver doesn't exists: " + path)
    return path


def get_raster_path_storage(layername, ext=".geotiff"):
    path = os.path.join(config["settings"]["folders"]["storage"], "raster",  layername, layername + ext)
    if not os.path.isfile(path):
        log.error("File on storage doesn't exists: " + path)
    return path


# TODO Here?
def _get_metadata_by_uid(uid, full=True, dsd=True):
    url = config["settings"]["metadata"]["url_get_metadata_uid"].replace("<uid>", uid)
    url += "?full=" + str(full) + "&dsd=" + str(dsd)
    r = requests.get(url)
    log.info(r.text)
    log.info(r.status_code)
    if r.status_code is not 200:
        raise Exception(r.text)
    return json.loads(r.text)