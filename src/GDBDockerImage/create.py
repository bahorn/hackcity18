import docker
import json
import random
import requests
import time
import sys


## This talks to the flask server defined in backend.
## We use the following endpoints:
### * /announce_session - Reveals we setup a container and what port we used.
### * /config/<instance_id> - Gets the ENV config for a testcase.
### * /new_jobs  - Gets all the new jobs, then removes them.
class DebuggerServerCreator:
    def __init__(self, master):
        # Our master node, used to get builds from.
        self._master = master
    # Probe the server to get the instances config, which is a list of ENV
    # variables used by the Docker container.
    def fetch_config(self, instance_id):
        r = requests.get('{}/config/{}'.format(self._master, instance_id))
        if r.status_code == 200:
            blob = r.json()['job']['testcase']['env']
            blob['SERVER'] = r.json()['job']['SERVER']
            blob['ID'] = r.json()['job']['ID']
            print(blob)
            return blob
        return None
    # create the instance.
    def create(self, instance_id, port=None):
        # We expose onto a random port.
        if port == None:
            port = random.randint(5000,8000)
        env = self.fetch_config(instance_id)
        if env == None:
            return None
        ports = {
            '1234':str(port)
        }
        c = docker.from_env()
        container = c.containers.run(
            image='gdbserver:latest',
            detach=True,
            privileged=True,
            ports=ports,
            environment=env
        )
        return (instance_id,port,container)
    # Let the server know we created it.
    def announce(self, instance):
        details = {
            "instance":instance[0],
            "port":instance[1]
        }
        print instance
        r = requests.post("{}/announce".format(self._master),
                          json=details)
        return r.json()
    # Check the queue.
    def check(self):
        r = requests.get("{}/new_jobs".format(self._master))
        new_jobs = r.json()
        print new_jobs
        for job in new_jobs['jobs']:
            new_instance = self.create(job['id'])
            if new_instance != None:
                self.announce(new_instance)
            # server would have removed them now.

if __name__ == "__main__":
    creator = DebuggerServerCreator(sys.argv[1])
    while True:
        creator.check()
        # Probe every 15 seconds.
        time.sleep(5)

