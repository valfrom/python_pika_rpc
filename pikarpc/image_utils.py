from PIL import Image
import io


def image_to_byte_array(image: Image, fmt=None):
    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format=image.format if fmt is None else fmt)
    return image_byte_array.getvalue()


def image_from_byte_array(data: bytes):
    io_data = io.BytesIO(data)
    im = Image.open(io_data)
    return im