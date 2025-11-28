import json
from kafka import KafkaConsumer, KafkaProducer
from sqlalchemy import create_engine, text
import pandas as pd


class UserConsumer:
    """
    Kafka consumer for the 'users' topic:
    - Validates messages
    - Writes valid messages to PostgreSQL
    - Sends invalid messages to a Dead Letter Queue (DLQ)
    """

    def __init__(self):
        """define atributes"""
        self.engine = create_engine(
            "postgresql+psycopg2://postgres:postgres@postgres:5432/stream"
        )
        self.list_fields = sorted(["user_id", "name", "email", "created_at"])

    def _start_up_sql(self):
        """Ensure the database schema and users table exist."""
        with self.engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS stream_target"))
            conn.execute(
                text("""
            CREATE TABLE IF NOT EXISTS stream_target.users (
                user_id BIGINT,
                name TEXT,
                email TEXT,
                created_at TEXT
            );
            """)
            )
            conn.commit()

    def _check_valid_message(self, message):
        """Return True if the message has all required fields."""
        columns = sorted(list(message.value.keys()))
        return columns == self.list_fields

    def __call__(self):
        """Main consumer loop: poll messages, validate, write valid to DB, send invalid to DLQ"""
        self._start_up_sql()
        self.dlq_producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        self.consumer = KafkaConsumer(
            "users",
            bootstrap_servers="kafka:9092",
            auto_offset_reset="earliest",
            value_deserializer=lambda v: json.loads(v),
            group_id="users_ingestion_group",
        )
        # number of messages per batch
        batch_size = 100
        while True:
            raw_messages = self.consumer.poll(timeout_ms=1000, max_records=batch_size)
            batch = []

            for tp, messages in raw_messages.items():
                for message in messages:
                    if self._check_valid_message(message):
                        batch.append(message.value)
                    else:
                        self.dlq_producer.send("dlq_users", message.value)

            # flush messages to dlq at the end of every batch just in case
            self.dlq_producer.flush()

            # check that the batch is not empty which is very unlikely
            if batch:
                df_users = pd.DataFrame(batch)
                df_users.to_sql(
                    "users",
                    self.engine,
                    schema="stream_target",
                    if_exists="append",
                    index=False,
                )
