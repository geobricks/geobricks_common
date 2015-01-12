import unittest
import os
import json
from geobricks_common.core.filesystem import get_raster_path, get_raster_path_published, get_raster_path_storage, get_raster_path_storage_by_uid, get_raster_path_published_by_uid



class GeobricksTest(unittest.TestCase):

    def test_get_raster_path(self):
        metadata = {
            "dsd": {
                "datasource": "storage",
                "layerName": "rice_area_4326"
            }
        }
        path = get_raster_path(metadata)
        self.assertEqual(os.path.isfile(path), True)

    def test_get_raster_path_published_by_uid(self):
        path = get_raster_path_published_by_uid("workspace:rice_area_3857")
        self.assertEqual(os.path.isfile(path), True)

    def test_get_raster_path_published(self):
        path = get_raster_path_published("workspace", "rice_area_3857")
        self.assertEqual(os.path.isfile(path), True)

    def test_get_raster_path_storage_by_uid(self):
        path = get_raster_path_storage_by_uid("rice_area_4326")
        self.assertEqual(os.path.isfile(path), True)

    def test_get_raster_path_storage(self):
        path = get_raster_path_storage("rice_area_4326")
        self.assertEqual(os.path.isfile(path), True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)


