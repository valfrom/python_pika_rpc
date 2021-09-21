import pika


class RpcServer:
    def __init__(self, queue_name='rpc_queue', host='localhost'):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=queue_name)

        def on_request(ch, method, props, body):
            response = self.process(body.decode("utf-8"))

            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id = props.correlation_id),
                             body=str(response))
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=on_request)

    def start(self):
        self.channel.start_consuming()

    def process(self, data):
        return data
