eventKafkaPostgres

A system that generates some events and passes the events through Aiven Kafka instance to Aiven PostgreSQL database. 

This includes:
1. Kafka producer which sends data to a Kafka topic,
2. Kafka consumer storing the data to Aiven PostgreSQL database.

**For this purpose, the following files have been created:**

**a. simpleEvents.py**

A simple event system in Python, capable of subscribing events and storing them in a subscriber list.
Although this system can be extended to much robust capabilities with messaging system and triggers using 
the Observer Pattern, the minimalistic implementation is enough for this project.

This file contains a Class EventSystem and it's methods add_event() and remove_event().


**b. kproducer.py**

In this file a Kafka Producer object is created that connects to the Aiven Kafka instance.
Producer object is created when the main() function is called.
 
This file also imports and implements EventSystem class and its add_event() method within 
bandwidth_exceed_event_system() function that, upon execution with main() function, generates 
Bandwidth Exceed waring logs (when the system bandwidth usage exceeds given limit(non-event range))
and registers those logs as events in the events subscription list of EventSystem's instance called 
bandwidth_exceeds. 

As well as those event logs are also broadcast using send() method of the Kafka Producer object kproducer.
Because the nature of this event is continuous (bandwidth checks run on second intervals continuously),
we deliver the messages from the queue in 120 seconds intervals using flush() method and break out of the loop. 
_This keeps the producer async and the value is customisable according to the requirement._
However, removing this provision can make create _sync producer, which is not a good idea._
 
main() function wraps the bandwidth_exceed_event_system() which is executed when the main() function executes.

**c. kconsumer.py**

This file instantiates Kafka Consumer object and connects to Aiven Kafka instance.
It consumes the message and records them in Aiven PostgreSQL database.
After the message is recorded, the database connection is closed.




**Additional files:**

\__init__.py

*setup.py*


