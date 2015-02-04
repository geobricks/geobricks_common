Geobricks Common
==============

Geobricks common library handle some functionalities that are used by different Geobricks components, like the logging, folders structure and email service.


# Installation

## Linux

```python

pip install geobrickscommon

```

## Example of configuration

An example of main configuration contained in geobricks.common.config.config:

```python
{

    "settings": {

            # Logging configurations
            "logging": {
                "level": logging.INFO,
                "format": "%(asctime)s | %(levelname)-8s | %(name)-20s | Line: %(lineno)-5d | %(message)s",
                "datefmt": "%d-%m-%Y | %H:%M:%s"
            },

            # Folders to be used by the system
            "folders": {
                "tmp": "/tmp",
                #"geoserver_datadir": "/tmp",
                "geoserver_datadir": "/geoserver_data_dir",
                "distribution": "/distribution_folder",
                "storage": "/storage_folder"
            },

            # Email configurations (for now uses gmail as default client)
            "email": {
                "user":  "user",
                "password": "password"
            },

            # optional metadata D3S service used to get a resource using its UID
            "metadata": {
                "url_get_metadata_uid": "http://localhost:7788/d3s/msd/resources/metadata/uid/<uid>",
            }
    }
}
```