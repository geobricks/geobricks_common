import unittest
import os
from geobricks_common.core.filesystem import get_raster_path, get_raster_path_published, get_raster_path_storage



class GeobricksTest(unittest.TestCase):

    def test_get_raster_path(self):
        metadata = {
            "dsd": {
                "datasource": "storage",
                "layerName": "rice_area_4326"
            }
        }
        path = get_raster_path(metadata)
        # this is used to normalize relative path used during test
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), path))
        self.assertEqual(os.path.isfile(path), True)

    def test_get_raster_path_published(self):
        path = get_raster_path_published("workspace", "rice_area_3857")
        # this is used to normalize relative path used during test
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), path))
        self.assertEqual(os.path.isfile(path), True)

    def test_get_raster_path_storage(self):
        path = get_raster_path_storage("rice_area_4326")
        # this is used to normalize relative path used during test
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), path))
        self.assertEqual(os.path.isfile(path), True)


def run_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_test()


