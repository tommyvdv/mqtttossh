import json
import ansible_runner

class Message():
    def __init__(self, topic, payload):
        self._topic = topic
        self._payload = payload

    def get_topic(self):
        return self._topic

    def get_payload(self):
        return self._payload

class CommandFactory():
    def __init__(self, project_dir, inventory):
        self._project_dir = project_dir
        self._inventory = inventory

    def create(self, message):
        return Command(message, self._project_dir, self._inventory)

    def __str__(self):
        return '{self._project_dir} {self._inventory}'

class Command():

    def __init__(self, message, project_dir, inventory):
        self._message = message
        self._target = payload_to_json(message).get('target')
        self._play = payload_to_json(message).get('play')
        self._project_dir = project_dir
        self._inventory = inventory

    def run(self, debug=False):
        run = ansible_runner.run(limit=f'{self._target}', playbook=f'{self._play}.yml', project_dir=self._project_dir, inventory=self._inventory)
        status = run.status
        return_code = run.rc
        stats = run.stats
        if debug:
            pretty = json.dumps(stats, indent=4, sort_keys=True)
            print(f"{status}: {return_code}")
            print("Final status:")
            print(pretty)
            for each_host_event in run.events:
                print(each_host_event['event'])
        return run

    def publish(self, client, topic, debug=False):
        payload = {
            'target': self._target,
            'play': self._play,
            'stats': self.run(debug).stats,
        }
        client.publish(Message(topic, dict_to_json_string(payload)))

    def __str__(self):
        return f'{self._target} {self._play}'

def payload_to_json(message):
    return json.loads(message.payload)

def dict_to_json_string(dictionary):
    return json.dumps(dictionary)
