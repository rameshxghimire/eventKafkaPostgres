"""
    kconsumer.py
    A kafka consumer that consumes the broadcast message, in this case bandwidth exceed alerts, and passes them on to
    Aiven PostgreSQL.
"""

# imports
from kafka import KafkaConsumer
import psycopg2


# create the consumer object
# topic : "bandwidth-exceeds"
consumer = KafkaConsumer(
    "bandwidth-exceeds",
    bootstrap_servers="kafka-ff4108e-rameshxghimire-92e4.aivencloud.com:27978",
    client_id="demo-client-1",
    group_id="demo-group",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
)


# establish the database connection
conn = connection = psycopg2.connect(user="avnadmin",
                                  password="nzvytb22k9e65qgd",
                                  host="pg-36c75f0b-rameshxghimire-92e4.aivencloud.com",
                                  port="27976",
                                  database="new_database")


# open a cursor
cur = conn.cursor()
print(connection.get_dsn_parameters())

# insert the message from consumer into the database
# database: defaultdb, table: bandwidth, column for record: message
for message_ in consumer:
    message_put = message_.value
    cur.execute("INSERT INTO bandwidth(message) VALUES (%s)", message_put)
    print(f"{message_put} added to the database")


# comment the changes
conn.commit()

# close the cursor
cur.close()

# close the connection
conn.close()
