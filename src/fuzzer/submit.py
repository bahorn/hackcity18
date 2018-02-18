import requests
import os
import copy
from datetime import datetime

# Upload our bugs to the server.

def get_date():
    return str(datetime.now())

class Submit:
    def __init__(self, name, master):
        self._master = master
        self._name = name
    def upload_testcase(self, filename):
        pass
    def upload(self,meta, file=None):
        env = copy.deepcopy(meta)
        if file != None:
            # upload the testcase somewhere.
            self.upload_testcase(file)
            env['TESTCASE'] = where_uploaded
        env['TARGET'] = self._name
        data = {
            "name":self._name,
            "env":env,
            "date":get_date()
        }
        r = requests.post("{}/testcases".format(self._master), json=data)
        return r.text

if __name__ == "__main__":
    submitter = Submit("testbin", "http://172.16.1.84:5000")
    meta = {
        'BINARY_SOURCE':'http://172.16.1.84:8000/testbin',
        'SETUP_SOURCE':'http://172.16.1.84:8000/setup.sh',
        'TRIGGER_SOURCE':'http://172.16.1.84:8000/trigger',
        'RUN_CMD':'/target/testbin',
        'TRIGGER':'trigger'
    }
    print submitter.upload(meta)
