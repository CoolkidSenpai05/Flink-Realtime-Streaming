from faker import Faker
from confluent_kafka import SerializingProducer

import random
import json
import time
from datetime import datetime


fake = Faker()

def generate_sales_transaction():
    user = fake.simple_profile()

    return {
        "transactionId": fake.uuid4(),
        "productId": random.choice([["product1", "product2", "product3"], ["product4", "product5", "product6"]]),
        "productName": random.choice(['laptop', 'mobile', 'tablet', 'watch', 'headphone', 'speaker']),
        "productCategory": random.choice(['electronics', 'fashion', 'grocery', 'home', 'beauty', 'sports']),
        "productPrice": round(random.uniform(10.0, 1000.0), 2),
        "productQuantity": random.randint(1, 10),
        'productBrand': random.choice(['apple', 'samsung', 'oneplus', 'mi', 'boat', 'sony']),
        'currency': random.choice(['USD', 'GBP']),
        'customerId': user['username'],
        'transactionDate': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        "paymentMethod": random.choice(['credit_card', 'debit_card', 'online_transfer'])
    }

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def main():
    topic = 'financial_transactions'
    producer = SerializingProducer({
        'bootstrap.servers': 'localhost:9092',
    })

    curr_time = datetime.now()

    while (datetime.now() - curr_time).seconds < 120:
        try:
            transaction = generate_sales_transaction()
            transaction['totalAmount'] = round(transaction['productPrice'] * transaction['productQuantity'], 2)
            print(f"Generated transaction: {transaction}")

            producer.produce(topic,
                             key=transaction['transactionId'],
                             value=json.dumps(transaction),
                             on_delivery=delivery_report
                             )
            producer.poll(0)

            # wait for 5 seconds before generating the next transaction
            time.sleep(5)

        except BufferError:
            print("Local producer queue is full, waiting for free space...")
            time.sleep(1)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
              