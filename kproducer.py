"""
    kproducer.py
    A kafka producer in that checks incoming and outgoing bandwidth usage every seconds and broadcasts
    when limit exceeds.

    Simple implementation of the event system generating message for broadcasting:
    - Every time the bandwidth exceeds the limit, a subscriber is added to events (subscriber list) attribute of
    the EventSystem object.
    Topic = "bandwidth-exceeds"
"""
# imports
import os
import sys
import psutil
from time import sleep
from kafka import KafkaProducer
from simpleEvents import EventSystem


def bandwidth_exceed_event_system(bandwidth_exceeds):
    """
    Checks the incoming and outgoing connection, determines the bandwidth uses and logs bandwidth exceeds time.
    For the sake of simplicity, bandwidth limit (non-event) is set to be less than 1024 bytes.
    :param bandwidth_exceeds: an objects of type EventSystem
    :return: None
    """
    old_value = 0
    at_sec = 0
    while True:
        new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

        value = new_value - old_value
        if value >= 1024:
            bandwidth_exceeds.add_event(f"at second: {at_sec}")
            print(f"Sending bandwidth excess record...")
            producer.send("bandwidth-exceeds", bandwidth_exceeds.events[-1].encode("utf-8"))
            print(bandwidth_exceeds.events[-1])
        # Let's deliver the messages in queue in 120 seconds intervals
        # Let's also add a break statement here for stopping the function, so that the system stays async.
        if at_sec == 120:
            producer.flush()
            break
        old_value = new_value
        sleep(1)
        at_sec += 1


# Wrap the above function in the main function.
def main():
    # run the function
    bandwidth_exceed_event_system(bandwidth_exceeds)


# run the main function
if __name__ == '__main__':
    # create the producer object
    producer = KafkaProducer(
        bootstrap_servers="kafka-ff4108e-rameshxghimire-92e4.aivencloud.com:27978",
        security_protocol="SSL",
        ssl_cafile="ca.pem",
        ssl_certfile="service.cert",
        ssl_keyfile="service.key",
    )

    # Create an EventSystem object to pass it to the bandwidth_exceed_event_system function
    bandwidth_exceeds = EventSystem()
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
