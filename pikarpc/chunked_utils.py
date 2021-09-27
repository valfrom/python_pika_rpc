from pikarpc.byte_utils import int_to_bytes, int_from_bytes


def chunked_bytes_from_dict(d: dict):
    result = bytes()
    for k, v in d.items():
        if type(v) == bytes:
            result += b'b'
            bts = v
        elif type(v) == str:
            result += b's'
            bts = v.encode('utf-8')

        kb = k.encode('utf-8')
        result += int_to_bytes(len(kb))
        result += kb

        result += int_to_bytes(len(bts))
        result += bts

    return result


def chunked_dict_from_bytes(b):
    result = {}
    index = 0
    while index < len(b):
        t = b[index:index+1].decode('utf-8')
        index += 1
        kl = int_from_bytes(b[index:index+4])
        index += 4
        k = b[index:index+kl].decode('utf-8')
        index += kl
        l = int_from_bytes(b[index:index+4])
        index += 4
        data = b[index:index+l]
        index += l
        if t == 's':
            data = data.decode('utf-8')

        result[k] = data

    return result
