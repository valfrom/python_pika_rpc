import requests
import uuid
from .chunked_utils import chunked_object_from_bytes


class RpcClient(object):

    def __init__(self, queue_name='rpc_queue', host='localhost', port=8001, timeout=120):
        self.queue_name = queue_name
        self.timeout = timeout
        self.host = host
        self.port = port

    def call(self, data):
        url = 'http://{0}:{1}/rpc/{2}'.format(self.host, self.port, self.queue_name)
        r = requests.post(url, data=data, headers={'id': str(uuid.uuid4())})
        return chunked_object_from_bytes(r.content)

    def send(self, data):
        url = 'http://{0}:{1}/rpc/{2}'.format(self.host, self.port, self.queue_name)
        requests.post(url, data=data, headers={'id': str(uuid.uuid4()),'type': 'async'})

