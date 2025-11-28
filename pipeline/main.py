from pipeline.stream import StreamEvents
from pipeline.user_consumer import UserConsumer
from pipeline.purchase_consumer import PurchaseConsumer
from multiprocessing import Process
import time
def main():
    
    print("Streaming started...", flush=True)
    stream_thread = Process(target=StreamEvents.generate_users)
    stream_thread.start()
    
    time.sleep(2)
    print(f"User Consumer started...", flush=True)
    user_consumer_thread = Process(target=UserConsumer())
    user_consumer_thread.start()


    time.sleep(5)
    print(f"Purchase Consumer started...", flush=True)
    purchase_consumer_thread = Process(target=PurchaseConsumer())
    purchase_consumer_thread.start()


main()