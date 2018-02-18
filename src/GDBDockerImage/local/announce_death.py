import os
import requests
kill_url = os.environ['SERVER']+'unannounce'
r = requests.post(kill_url, json={"id":os.environ['ID']})
print("KILLED")
