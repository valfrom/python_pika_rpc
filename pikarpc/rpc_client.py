import requests
import uuid


class RpcClient(object):

    def __init__(self, queue_name='rpc_queue', host='localhost', port=8001, timeout=120):
        self.queue_name = queue_name
        self.timeout = timeout
        self.host = host
        self.port = port

    def call(self, data):
        url = 'http://{0}:{1}/rpc/{2}'.format(self.host, self.port, self.queue_name)
        r = requests.post(url, data=data, headers={'id': str(uuid.uuid4())})
        print('Response: ' + str(r))
        print('URL: ' + url)
        return r.content

    def send(self, data):
        url = 'http://{0}:{1}/rpc/{2}'.format(self.host, self.port, self.queue_name)
        requests.post(url, data=data, headers={'id': str(uuid.uuid4()),'type': 'async'})

