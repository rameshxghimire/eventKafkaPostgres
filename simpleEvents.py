"""
    simpleEvents.py
    A very simple event system in Python which can be extended and used with other systems such as messaging systems.
"""

class EventSystem:
    """
    blueprint for simpleEvents objects.
    """
    def __init__(self, events=[]):
        self.events = events

    def add_event(self, event):
        self.events.append(event)
        return self.events

    def remove_event(self, event):
        self.events.remove(event)
        return self.events
