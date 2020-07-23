import time
import ray
ray.init()
@ray.remote
class MessageActor(object):
    def __init__(self):
        self.messages = []
    def add_message(self, message):
        self.messages.append(message)
    def get_and_clear_messages(self):
        messages = self.messages
        self.messages = []
        return messages
# Define a remote function which loops around and pushes
# messages to the actor.
@ray.remote
def worker(message_actor, j):
    for i in range(100):
        time.sleep(1)
        message_actor.add_message.remote(
            "Message {} from worker {}.".format(i, j))
# Create a message actor.
message_actor = MessageActor.remote()
# Start 3 tasks that push messages to the actor.
[worker.remote(message_actor, j) for j in range(3)]
# Periodically get the messages and print them.
for _ in range(100):
    new_messages = ray.get(message_actor.get_and_clear_messages.remote())
    print("New messages:", new_messages)
    time.sleep(1)
"""
output:
New messages: []
New messages: ['Message 0 from worker 0.', 'Message 0 from worker 1.', 'Message 0 from worker 2.']
New messages: ['Message 1 from worker 0.', 'Message 1 from worker 1.', 'Message 1 from worker 2.']
New messages: ['Message 2 from worker 0.', 'Message 2 from worker 1.', 'Message 2 from worker 2.']
New messages: ['Message 3 from worker 0.', 'Message 3 from worker 1.', 'Message 3 from worker 2.']
New messages: ['Message 4 from worker 0.', 'Message 4 from worker 2.', 'Message 4 from worker 1.']
New messages: ['Message 5 from worker 0.', 'Message 5 from worker 1.', 'Message 5 from worker 2.']
New messages: ['Message 6 from worker 0.', 'Message 6 from worker 1.', 'Message 6 from worker 2.']
New messages: ['Message 7 from worker 0.', 'Message 7 from worker 2.', 'Message 7 from worker 1.']
New messages: ['Message 8 from worker 0.', 'Message 8 from worker 2.', 'Message 8 from worker 1.']
New messages: ['Message 9 from worker 0.', 'Message 9 from worker 1.', 'Message 9 from worker 2.']
New messages: ['Message 10 from worker 0.', 'Message 10 from worker 2.', 'Message 10 from worker 1.']
New messages: ['Message 11 from worker 0.', 'Message 11 from worker 2.', 'Message 11 from worker 1.']
New messages: ['Message 12 from worker 0.', 'Message 12 from worker 1.', 'Message 12 from worker 2.']
"""