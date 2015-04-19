# -*- coding: utf-8 -*-
from carrot.connection import BrokerConnection
from carrot.messaging import Publisher
from scrapy import signals
from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet.threads import deferToThread

# Credit: https://gist.github.com/abevoelker/10606489
class RabbitMQPipeline(object):
    def __init__(self, hostname, port, user_id, password, virtual_host, encoder_class):
        self.queue_connection = BrokerConnection(
            hostname=hostname,
            port=port,
            userid=user_id,
            password=password,
            virtual_host=virtual_host
        )

        self.encoder = encoder_class()

        # Setup / Teardown Rabbit plumbing when spider opens / closes
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    @classmethod
    def from_settings(cls, settings):
        hostname      = settings.get('BROKER_HOST')
        port          = settings.get('BROKER_PORT')
        user_id       = settings.get('BROKER_USERID')
        password      = settings.get('BROKER_PASSWORD')
        virtual_host  = settings.get('BROKER_VIRTUAL_HOST')
        encoder_class = settings.get('QUEUE_SERIALIZER', ScrapyJSONEncoder)

        return cls(hostname, port, user_id, password, virtual_host, encoder_class)

    def spider_opened(self, spider):
        self.publisher = Publisher(
            connection=self.queue_connection,
            exchange='',
            routing_key=spider.name
        )

    def spider_closed(self, spider):
        self.publisher.close()

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        self.publisher.send(self.encoder.encode(dict(item)))
        return item
