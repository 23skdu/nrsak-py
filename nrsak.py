#!/usr/bin/env python3
import inspect, sys, os, argparse, requests
try:
  nrkey = os.environ["NR_KEY"]
except:
  print("you must have NR_KEY environment variable set")
  sys.exit(1)

nrapi = 'https://api.newrelic.com/v2/'
nrnerd = 'https://api.newrelic.com/graphql'

parser = argparse.ArgumentParser()
parser.add_argument("action")
args = parser.parse_args()
action=args.action

def function_list():
  for name, data in inspect.getmembers(sys.modules['__main__'], inspect.isfunction):
    if name.startswith('nr'):
      print(name)

def nrSummary():
  result = requests.get(nrapi+"applications.json", headers={"Api-Key":nrkey})
  if result.status_code == 200:
    print(result.text)
  else:
    print("Error: {result.status_code}")
    print(result.request.headers)
    sys.exit(1)

eval(action+'()')
