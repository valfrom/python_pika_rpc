import unittest
from pikarpc.chunked_utils import *
from pikarpc.image_utils import *
from PIL import Image
import numpy as np


class Test(unittest.TestCase):
    def test_chunked(self):
        d = {"k1": "123", "k2": b'bytes'}

        bts = chunked_bytes_from_object(d)
        d2 = chunked_object_from_bytes(bts)

        self.assertEqual(d, d2)

    def test_chunked_int(self):
        d = {"k1": 123, "k2": 1}

        bts = chunked_bytes_from_object(d)
        d2 = chunked_object_from_bytes(bts)

        self.assertDictEqual(d, d2)

    def test_chunked_bool(self):
        d = {"k1": True, "k2": 1}

        bts = chunked_bytes_from_object(d)
        d2 = chunked_object_from_bytes(bts)

        self.assertDictEqual(d, d2)

    def test_chunked_float(self):
        d = {"k1": 123.00012, "k2": 17.00019}

        bts = chunked_bytes_from_object(d)
        d2 = chunked_object_from_bytes(bts)

        self.assertAlmostEqual(d['k1'], d2['k1'], 5)
        self.assertAlmostEqual(d['k2'], d2['k2'], 5)

    def test_chunked_sub(self):
        d = {"k1": "123", "k2": b'bytes', "d": {"k3": "v3", "k4": 123}}

        bts = chunked_bytes_from_object(d)
        d2 = chunked_object_from_bytes(bts)

        self.assertEqual(d, d2)

    def test_chunked_dict_in_list(self):
        d = {"k1": "123", "k2": b'bytes', "a": [1, 2, 3, 4, 5]}

        bts = chunked_bytes_from_object(d)
        d2 = chunked_object_from_bytes(bts)

        self.assertEqual(d, d2)

    def test_chunked_list(self):
        l1 = [1, 2, 3, 4, {'k1': [9, 8, 7]}]

        bts = chunked_bytes_from_object(l1)
        l2 = chunked_object_from_bytes(bts)

        self.assertEqual(l1, l2)

    def test_image(self):
        im = Image.open('../test_data/Lenna.png')
        bts = image_to_byte_array(im, 'PNG')
        im2 = image_from_byte_array(bts)
        self.assertEqual(im.size, im2.size)

        im = np.asarray(im)
        im2 = np.asarray(im2)
        np.testing.assert_equal(im, im2)

    def test_chunked_image(self):
        im = Image.open('../test_data/Lenna.png')
        d = {'image': im}

        bts = chunked_bytes_from_object(d, lossless=True)
        d2 = chunked_object_from_bytes(bts)

        im2 = d2['image']

        im = np.asarray(im)
        im2 = np.asarray(im2)
        np.testing.assert_equal(im, im2)


if __name__ == '__main__':
    unittest.main()
