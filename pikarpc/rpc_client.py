import requests
import uuid


class RpcClient(object):

    def __init__(self, queue_name='rpc_queue', host='localhost', port=8001, timeout=120):
        self.queue_name = queue_name
        self.timeout = timeout
        self.host = host
        self.port = port

    def call(self, data: str):
        url = 'http://{0}:{1}/rpc/{2}'.format(self.host, self.port, self.queue_name)
        r = requests.post(url, json={'id': str(uuid.uuid4()), 'data': data})
        print('Response: ' + str(r))
        print('URL: ' + url)
        result = r.json()['result']
        return result

    def send(self, data: str):
        url = 'http://{0}:{1}/rpc/{2}'.format(self.host, self.port, self.queue_name)
        requests.post(url, json={'id': str(uuid.uuid4()), 'data': data}, headers={'type': 'async'})

