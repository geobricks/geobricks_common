import logging
import os
from geobricks_common.core.utils import dict_merge
import simplejson

config = {

    "settings": {

        # it is used to have a common configuration file to use
        "path_common_settings_file": "../../../geobricks_common_settings.json",

        # Logging configurations
        "logging": {
            "level": logging.INFO,
            "format": "%(asctime)s | %(levelname)-8s | %(name)-20s | Line: %(lineno)-5d | %(message)s",
            "datefmt": "%d-%m-%Y | %H:%M:%s"
        },

        # Folders
        "folders": {
            "tmp": "/tmp",
            #"geoserver_datadir": "../test_data/geoserver_data_dir",
            "geoserver_datadir": "/home/vortex/programs/SERVERS/tomcat_geoservers/geoserver_data_2_5_3/data/",
            "distribution": "../test_data/distribution",
            "storage": "../test_data/storage",
            # this is used by the filesystem to get the (published) layers in the file system
            "workspace_layer_separator": ":"
        },

        # Email configurations (for now uses gmail as default client)
        "email": {
            "user":  "user",
            "password": "password"
        },

        "metadata": {
            "url_get_metadata_uid": "http://fenix.fao.org/d3s_dev/msd/resources/metadata/uid/<uid>",
        }
    }

}

def merge_config_from_file(config_to_merge, path_common_settings_file=None):
    if path_common_settings_file is None:
        if not "path_common_settings_file" in config["settings"]:
            # no possible merges
            return config_to_merge
        if "path_common_settings_file" in config["settings"]:
            return merge_file(config_to_merge, config["settings"]["path_common_settings_file"])
    else:
        return merge_file(config_to_merge, path_common_settings_file)


def merge_file(config_to_merge, path_common_settings_file):
    print path_common_settings_file
    if os.path.isfile(path_common_settings_file):
        with open(path_common_settings_file) as data_file:
            common_settings = simplejson.load(data_file)
            config_to_merge["settings"] = dict_merge(common_settings, config_to_merge)
            config_to_merge["settings"] = config_to_merge["settings"]["settings"]
            return config_to_merge
    else:
        # no possible merges (file doesn't exists)
        return config_to_merge


# merge config file if exists
#merge_config_from_file(config)


