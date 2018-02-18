import requests
import json
import time

master = "http://172.16.1.84:5000"

class ListTestcases(GenericCommand):
    """Auto cr"""
    _cmdline_ = "list_testcases"
    _syntax_  = "{:s}".format(_cmdline_)

    def do_invoke(self, argv):
        r = requests.get("{}/testcases".format(master))
        print("[!] Testcases in Fuzzer logs")
        for testcase in r.json()['testcases']:
            print("[!] {} {} {}".format(
                testcase['id'], testcase['name'], testcase['date']))

class SetupSession(GenericCommand):
    """ Setups up a debugging session """
    _cmdline_ = "setup_session"
    _syntax_  = "{:s}".format(_cmdline_)

    def do_invoke(self, argv):
        if len(argv) != 1:
            print("[!] Usage: {} <testcase id>".format(_cmdline_))
            return
        job = {'testcase':argv[0]}
        r = requests.post("{}/new_jobs".format(master), json=job)
        if r.json()['status'] != 'ok':
            print("[!] Invalid Job Id")
            return
        session_id = r.json()['id']
        print(session_id)
        print("[!] Waiting for session to start!")
        while True:
            r = requests.get('{}/sessions/{}'.format(master, session_id))
            if r.json()['status'] == 'ok':
                break
            time.sleep(5)
        # now we can connect
        info = r.json()['session']
        host = "{}:{}".format(info['remote'],info['port'])
        gdb.execute("target remote {}".format(host))
        return

class TriggerTestcase(GenericCommand):
    """ Setups up a debugging session """
    _cmdline_ = "trigger_testcase"
    _syntax_  = "{:s}".format(_cmdline_)

    def do_invoke(self, argv):
        gdb.execute('c')
        return


class TagTestcase(GenericCommand):
    """ Setups up a debugging session """
    _cmdline_ = "tag_testcase"
    _syntax_  = "{:s}".format(_cmdline_)

    def do_invoke(self, argv):
        # Tag this bug.
        return



register_external_command(ListTestcases())
register_external_command(SetupSession())
#register_external_command(TagTestcase())
register_external_command(TriggerTestcase())
