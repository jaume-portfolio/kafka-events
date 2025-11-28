from pipeline.stream import StreamEvents
from pipeline.user_consumer import UserConsumer
from pipeline.purchase_consumer import PurchaseConsumer
from multiprocessing import Process
import time


def main():
    """
    Start the full streaming pipeline:
    - Launches Kafka producer to generate users and purchases
    - Starts user consumer after 2 seconds
    - Starts purchase consumer after 5 seconds
    - Uses multiprocessing to run producer and consumers concurrently
    """
    print("Streaming started...", flush=True)
    stream_thread = Process(target=StreamEvents.generate_users)
    stream_thread.start()

    time.sleep(2)
    print("User Consumer started...", flush=True)
    user_consumer_thread = Process(target=UserConsumer())
    user_consumer_thread.start()

    time.sleep(5)
    print("Purchase Consumer started...", flush=True)
    purchase_consumer_thread = Process(target=PurchaseConsumer())
    purchase_consumer_thread.start()


main()
