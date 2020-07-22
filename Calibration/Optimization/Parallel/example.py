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

@ray.remote
def run_sim(sim_params,sim_length,num_samples_from_end):
	sim_results = hc.HighwayCongested(wave_params=sim_params,sim_length=sim_length)
	sim_speeds = np.array(sim_results.getVelocityData())
	sim_speeds = sim_speeds[-num_samples_from_end:]
	total_sim_runs += 1
	print('Parameter values: a: '+str(sim_params[0])+' b: '+str(sim_params[1]) + ', simulation number: '+str(total_sim_runs))
	return sim_speeds

for a in a_range:
	for b in b_range:
		sim_params = [a,b]
		speed_vals = check_for_existing_csv(sim_params)
		for i in range(num_samples):
			speed_vals.append(run_sim.remote(sim_params,sim_length,num_samples_from_end))
		speed_vals = np.array(speed_vals)
		file_name  = 'a-'+str(a)+'b-'+str(b)+'.csv'
		np.savetxt(folder_path+file_name,speed_vals)
