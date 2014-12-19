import logging

config = {

    "settings": {
        # Logging configurations
        "logging": {
            "level": logging.INFO,
            "format": "%(asctime)s | %(levelname)-8s | %(name)-20s | Line: %(lineno)-5d | %(message)s",
            "datefmt": "%d-%m-%Y | %H:%M:%s"
        },
    },

    # Folders
    "folders": {
        "tmp": "tmp_path",
        "geoserver_datadir": "geoserver_data_folder",
        "distribution": "distribution_folder",
        "ftp": "ftp_folder",
        # this is used by the filesystem to get the (published) layers in the file system
        "workspace_layer_separator": "|"
    },

    # Email configurations (for now uses gmail as default client)
    "email": {
        "user":  "user",
        "password": "password"
    },

}
