import os
import tempfile
import uuid
import zipfile
import shutil
from geobricks_common.config.config import config

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
    :param extension: i.e. "tif"
    :param subfolder: "modis_folder"
    :param filename: "modis"
    :param add_uuid: add or not a uuid to the file
    :param folder_tmp: if not specified it takes the default tmp folder of the os.
    :return: a path to a tmp file
    """

    """
    Create the path for a tmp file and filename

    @type path: string
    @param path: path from the tmp folder
    @type extension: extension
    @param extension: i.e. .geotiff
    """
    if extension != '' and "." not in extension: extension = "." + extension
    folder_path = os.path.join(folder_tmp, subfolder)
    if subfolder is not '':
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


def get_raster_path(raster):
    uid = raster["uid"] if "uid" in raster else None
    isSTORAGE = False if "isFTP" not in raster else raster["isFTP"]
    workspace = raster["workspace"] if "workspace" in raster else None
    layername = raster["layerName"] if "layerName" in raster else None
    path = raster["path"] if "path" in raster else None

    if path is not None:
        return path

    if isSTORAGE is False:
        if uid is None:
            return get_raster_path_published(workspace, layername)
        else:
            return get_raster_path_published_by_uid(uid)

    elif isSTORAGE is True:
        if uid is None:
            return get_raster_path_storage(layername)
        else:
            return get_raster_path_storage_by_uid(uid)

    return None


# TODO: move it to the data manager?
def get_raster_path_published_by_uid(uid, ext=".geotiff"):
    l = uid.split(workspace_layer_separator) if workspace_layer_separator in uid else uid.split(":")
    return os.path.join(config["settings"]["folders"]["geoserver_datadir"], "data",  l[0], l[1], l[1] + ext);


def get_raster_path_published(workspace, layername, ext=".geotiff"):
    return os.path.join(config["settings"]["folders"]["geoserver_datadir"], "data",  workspace, layername, layername + ext);


def get_raster_path_storage(layername, ext=".geotiff"):
    return os.path.join(config["settings"]["folders"]["storage"], "raster",  layername, layername + ext);


# TODO not used
def get_raster_path_storage_by_uid(uid, ext=".geotiff"):
    return os.path.join(config["settings"]["folders"]["storage"], "raster", uid, uid + ext)


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


def make_archive(dir_to_zip, output_filename, archive_type='zip'):
    shutil.make_archive(output_filename, archive_type, dir_to_zip)


def get_filename(filepath, extension=False):
    drive, path = os.path.splitdrive(filepath)
    path, filename = os.path.split(path)
    name = os.path.splitext(filename)[0]
    if extension is True:
        return path, filename, name
    else:
        return name


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