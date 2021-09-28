import requests
from .chunked_utils import chunked_bytes_from_object, chunked_object_from_bytes


class RpcServer:
    def __init__(self, queue_name='rpc_queue', host='localhost', port=8001):
        self.queue_name = queue_name
        self.host = host
        self.port = port

    def wait(self):
        url = 'http://{0}:{1}/rpc/{2}'.format(self.host, self.port, self.queue_name)
        requests.post(url, headers={'type': 'get'})

    def start(self):
        url = 'http://{0}:{1}/rpc/{2}'.format(self.host, self.port, self.queue_name)
        while True:
            req = requests.post(url, headers={'type': 'get'})
            result = chunked_bytes_from_object(self.process(chunked_object_from_bytes(req.content)))
            requests.post('http://{0}:{1}/'.format(self.host, self.port), data=result, headers={'id': req.headers['id'], 'type': 'result'})

    def process(self, data):
        return data
