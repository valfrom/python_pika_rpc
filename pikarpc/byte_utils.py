import numpy


def int_to_bytes(v):
    b = bytearray(4)
    pack_int_to_array(b, 0, v)
    return b


def int_from_bytes(b):
    return numpy.frombuffer(b, dtype=numpy.int32)[0]


def float_to_bytes(v):
    b = bytearray(4)
    pack_float_to_array(b, 0, v)
    return b


def float_from_bytes(b):
    return numpy.frombuffer(b, dtype=numpy.float32)[0]


def half_float_to_bytes(v):
    b = bytearray(2)
    pack_half_float_to_array(b, 0, v)
    return b


def string_to_bytes(s):
    sb = bytearray(s, encoding="utf8")
    b = bytearray(4)
    pack_int_to_array(b, 0, len(sb))
    b.extend(sb)
    return b

def pack_float_to_array(data, offset, val):
    v = numpy.float32(val)
    b = numpy.array([v]).tobytes()

    for i in range(0, len(b)):
        data[offset + i] = b[i]

    return len(b)


def pack_half_float_to_array(data, offset, val):
    v = numpy.float16(val)
    b = numpy.array([v]).tobytes()

    for i in range(0, len(b)):
        data[offset + i] = b[i]

    return len(b)


def pack_int_to_array(data, offset, val):
    v = numpy.int32(val)
    b = numpy.array([v]).tobytes()
    for i in range(0, len(b)):
        data[offset + i] = b[i]

    return len(b)


def pack_half_int_to_array(data, offset, val):
    v = numpy.int16(val)
    b = numpy.array([v]).tobytes()
    for i in range(0, len(b)):
        data[offset + i] = b[i]

    return len(b)