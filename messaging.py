import pika
import uuid
import json

# Camada de mensageria baseada em RabbitMQ com operacoes RPC simples

class MessagingSystem:
    def __init__(self):
        # Abre conexao blocking e canal compartilhado para todas as chamadas do cliente
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

    def listen_and_reply(self, queue_name, callback_function):
        # Declara fila, processa mensagens sequenciais e devolve resposta serializada
        self.channel.queue_declare(queue=queue_name)

        def on_request(ch, method, props, body):
            request_data = json.loads(body)
            print(f"Recebido: {request_data}")

            # Executa a logica do servico e publica a resposta para a fila de retorno
            response_data = callback_function(request_data)

            ch.basic_publish(
                exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(
                    correlation_id=props.correlation_id
                ),
                body=json.dumps(response_data)
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("Resposta enviada.")

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=on_request)
        
        print(f"Aguardando requisições em '{queue_name}'...")
        self.channel.start_consuming()

    def call_rpc(self, queue_name, message_body):
        # Cria fila exclusiva para receber a resposta e publica a requisicao RPC
        result = self.channel.queue_declare(queue='', exclusive=True)
        callback_queue = result.method.queue

        self.response = None
        self.corr_id = str(uuid.uuid4())

        def on_response(ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = json.loads(body)

        self.channel.basic_consume(
            queue=callback_queue,
            on_message_callback=on_response,
            auto_ack=True
        )

        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            properties=pika.BasicProperties(
                reply_to=callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message_body)
        )

        # Aguarda ate que uma resposta com o mesmo correlation id chegue
        while self.response is None:
            self.connection.process_data_events()
            
        return self.response