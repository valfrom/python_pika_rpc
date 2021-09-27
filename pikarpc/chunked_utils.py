from pikarpc.byte_utils import int_to_bytes, int_from_bytes, float_to_bytes, float_from_bytes
from PIL import Image
from pikarpc.image_utils import image_from_byte_array, image_to_byte_array


def bytes_from_value(v, lossless):
    result = bytes()
    if type(v) == bytes:
        result += b'b'
        result += v
    elif type(v) == str:
        result += b's'
        result += v.encode('utf-8')
    elif type(v) == bool:
        result += b'v'
        result += int_to_bytes(1 if v else 0)
    elif type(v) == int:
        result += b'i'
        result += int_to_bytes(v)
    elif type(v) == float:
        result += b'f'
        result += float_to_bytes(v)
    elif type(v) == list:
        result += b'l'
        result += chunked_bytes_from_list(v, lossless)
    elif type(v) == dict:
        result += b'd'
        result += chunked_bytes_from_dict(v, lossless)
    elif issubclass(type(v), Image.Image):
        result += b'p'
        result += image_to_byte_array(v, fmt='PNG' if lossless else 'JPEG')

    return result


def value_from_bytes(b, index):
    l = int_from_bytes(b[index:index + 4])
    index += 4
    t = b[index:index + 1].decode('utf-8')
    index += 1
    data = b[index:index + l]
    index += l
    val = data
    if t == 's':
        val = data.decode('utf-8')
    elif t == 'v':
        val = True if int_from_bytes(data) == 1 else False
    elif t == 'i':
        val = int_from_bytes(data)
    elif t == 'f':
        val = float_from_bytes(data)
    elif t == 'd':
        val = chunked_dict_from_bytes(data)
    elif t == 'l':
        val = chunked_list_from_bytes(data)
    elif t == 'p':
        val = image_from_byte_array(data)

    return index, val


def chunked_bytes_from_object(o, lossless=False):
    result = bytes()
    if type(o) == dict:
        result += b'd'
        result += chunked_bytes_from_dict(o, lossless)
    elif type(o) == list:
        result += b'l'
        result += chunked_bytes_from_list(o, lossless)

    return result


def chunked_bytes_from_list(arr, lossless):
    result = bytes()
    result += int_to_bytes(len(arr))
    for v in arr:
        bts = bytes_from_value(v, lossless)
        result += int_to_bytes(len(bts) - 1)
        result += bts
    return result


def chunked_bytes_from_dict(d: dict, lossless):
    result = bytes()
    for k, v in d.items():
        bts = bytes_from_value(v, lossless)

        kb = k.encode('utf-8')
        result += int_to_bytes(len(kb))
        result += kb

        result += int_to_bytes(len(bts) - 1)
        result += bts

    return result


def chunked_object_from_bytes(b):
    t = b[0:1]
    if t == b'd':
        return chunked_dict_from_bytes(b[1:])
    elif t == b'l':
        return chunked_list_from_bytes(b[1:])

    return None


def chunked_list_from_bytes(b):
    result = []
    index = 0
    l = int_from_bytes(b[:4])
    index += 4
    for i in range(0, l):
        index, val = value_from_bytes(b, index)
        result.append(val)

    return result


def chunked_dict_from_bytes(b):
    result = {}
    index = 0
    while index < len(b):
        kl = int_from_bytes(b[index:index + 4])
        index += 4
        key = b[index:index + kl].decode('utf-8')
        index += kl

        index, val = value_from_bytes(b, index)
        result[key] = val

    return result
