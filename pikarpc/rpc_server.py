import requests


class RpcServer:
    def __init__(self, queue_name='rpc_queue', host='localhost', port=8001):
        self.queue_name = queue_name
        self.host = host
        self.port = port

    def wait(self):
        url = 'http://{0}:{1}/rpc/{2}'.format(self.host, self.port, self.queue_name)
        requests.post(url, headers={'type': 'get'}).json()

    def start(self):
        url = 'http://{0}:{1}/rpc/{2}'.format(self.host, self.port, self.queue_name)
        while True:
            req = requests.post(url, headers={'type': 'get'}).json()
            result = self.process(req['data'])
            response = {
                'id': req['id'],
                'result': result
            }
            requests.post('http://{0}:{1}/'.format(self.host, self.port), json=response, headers={'type': 'result'})

    def process(self, data):
        return data
