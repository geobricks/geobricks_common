import logging


config = {

    # To be used by Flask: DEVELOPMENT ONLY
    "debug": True,

    # Flask host: DEVELOPMENT ONLY
    "host": "localhost",

    # Flask port: DEVELOPMENT ONLY
    "port": 5907,

    "settings": {
        # Logging configurations
        "logging": {
            "level": logging.INFO,
            "format": "%(asctime)s | %(levelname)-8s | %(name)-20s | Line: %(lineno)-5d | %(message)s",
            "datefmt": "%d-%m-%Y | %H:%M:%s"
        },

        # Folders
        "folders": {
            "tmp": "/tmp",
            "geoserver_datadir": "../tests/data/geoserver_data_dir/",
            "storage": "../tests/data/storage/",
            # this is used by the filesystem to get the (published) layers in the file system
            "workspace_layer_separator": ":"
        },

        # Email configurations (for now uses gmail as default client)
        "email": {
            "user":  "user",
            "password": "password"
        },

        "metadata" : {
            "url_get_metadata_uid": "http://fenix.fao.org/d3s_dev/msd/resources/metadata/uid/<uid>",
        }
    }

}


