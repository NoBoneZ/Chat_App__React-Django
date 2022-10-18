import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ConversationConsumer(WebsocketConsumer):
    def connect(self):
        self.conversation = "pk"

        async_to_sync(self.channel_layer.conversation_add)(
            self.conversation,
            self.channel_name

        )

        self.accept()

        # self.send(text_data=json.dumps({
        #     "type": 'connection established',
        #     "message": 'You are now Connected'
        # }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.conversation_send)(
            self.conversation,
            {
                "type": 'conversation_message',
                'message': message

            }
        )

    def conversation_message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps(({
            "type": "conversation",
            'message': message
        })))


        # print(message)
        #
        # self.send(text_data=json.dumps({
        #     "type": 'chat',
        #     'message': message
        # }))
