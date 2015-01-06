import unittest
import os
from geobricks_common.core.filesystem import get_raster_path_published, get_raster_path_storage, get_raster_path_storage_by_uid, get_raster_path_published_by_uid



class GeobricksTest(unittest.TestCase):

    def test_get_raster_path_published_by_uid(self):
        path = get_raster_path_published_by_uid("test:mod13a2_3857")
        self.assertEqual(os.path.isfile(path), True)

    def test_get_raster_path_published(self):
        path = get_raster_path_published("test", "mod13a2_3857")
        self.assertEqual(os.path.isfile(path), True)

    def test_get_raster_path_storage_by_uid(self):
        path = get_raster_path_storage_by_uid("mod13a2_3857")
        self.assertEqual(os.path.isfile(path), True)

    def test_get_raster_path_storage(self):
        path = get_raster_path_storage("mod13a2_3857")
        self.assertEqual(os.path.isfile(path), True)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GeobricksTest)
    unittest.TextTestRunner(verbosity=2).run(suite)