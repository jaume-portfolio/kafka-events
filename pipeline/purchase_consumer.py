import json
from kafka import KafkaConsumer
from sqlalchemy import create_engine, text
import pandas as pd
import time

class PurchaseConsumer:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://postgres:postgres@postgres:5432/stream")        

    def _start_up_sql(self):
        # Create schema if it doesn't exist
        with self.engine.connect() as conn:
            conn.execute(text("""
            create table stream_target.purchases
            (
                id           bigint,
                user_id      bigint,
                product_name text,
                quantity_kg  double precision,
                total_price  double precision,
                created_at   text
            );
            """))
            conn.commit()

    def __call__(self):
        self._start_up_sql()
        self.consumer = KafkaConsumer(
            'purchases',
            bootstrap_servers='kafka:9092',
            auto_offset_reset='earliest',
            value_deserializer=lambda v: json.loads(v),
            group_id='purchases_ingestion_group'
        )

        batch_size = 100  # number of messages per batch
        while True:

            raw_messages = self.consumer.poll(timeout_ms=1000, max_records=batch_size)
            
            batch = []
            for tp, messages in raw_messages.items():
                for message in messages:
                    batch.append(message.value)

            df_purchases = pd.DataFrame(batch)

            df_purchases.to_sql('purchases', self.engine, schema='stream_target',if_exists='append', index=False)


    

