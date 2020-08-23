#!/usr/bin/env python3


from logging import basicConfig, INFO

from src.queue.consumer import Consumer

basicConfig(level=INFO)

if __name__ == "__main__":
    consumer = Consumer()
    consumer.start_consuming()
