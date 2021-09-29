import requests
from .chunked_utils import chunked_bytes_from_object, chunked_object_from_bytes


class RpcServer:
    def __init__(self, queue_name='rpc_queue', host='localhost', port=8001, timeout=120):
        self.queue_name = queue_name
        self.host = host
        self.port = port
        self.timeout = timeout

    def wait(self):
        url = 'http://{0}:{1}/rpc/{2}'.format(self.host, self.port, self.queue_name)
        try:
            requests.post(url, headers={'type': 'get'}, timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            pass
        except:
            pass

    def start(self):
        url = 'http://{0}:{1}/rpc/{2}'.format(self.host, self.port, self.queue_name)
        while True:
            try:
                req = requests.post(url, headers={'type': 'get'}, timeout=self.timeout)
                result = chunked_bytes_from_object(self.process(chunked_object_from_bytes(req.content)))
                requests.post('http://{0}:{1}/'.format(self.host, self.port), data=result,
                              headers={'id': req.headers['id'], 'type': 'result'}, timeout=self.timeout)
            except requests.exceptions.RequestException as e:
                pass
            except:
                pass

    def process(self, data):
        return data
