import pika
import uuid


class RpcClient(object):
    response = None
    corr_id = None

    def __init__(self, queue_name='rpc_queue', host='localhost'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))

        self.channel = self.connection.channel()
        self.queue_name = queue_name

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode("utf-8")

    def call(self, data: str):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=data)
        while self.response is None:
            self.connection.process_data_events()
        return self.response
