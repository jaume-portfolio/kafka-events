import json
from kafka import KafkaProducer
from pipeline.users import GenerateUser
from pipeline.purchases import GeneratePurchase


class StreamEvents:
    """
    Kafka event producer:
    - Generates random users and purchases
    - Sends them to 'users' and 'purchases' topics
    """

    @staticmethod
    def generate_users():
        """
        Generate and stream users and purchases:
        - Produces 100,000 users
        - For each user, generates one purchase
        - Sends data to Kafka with JSON serialization
        """
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        counter = 0
        generator = GenerateUser()

        while counter < 100000:
            # users
            user = generator()
            # print(user.name)
            producer.send("users", user)

            # purchase
            purchase = GeneratePurchase(user_id=user["user_id"])()
            # print(purchase.product_name)
            producer.send("purchases", purchase)

            producer.flush()
            # time.sleep(0.00001)
            counter = counter + 1
