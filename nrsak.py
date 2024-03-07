#!/usr/bin/env python3
import sys, os, argparse, re, requests
try:
  nrkey = os.environ["NR_KEY"]
except:
  print("you must have NR_KEY environment variable set")
  sys.exit(1)

valid_actions = [ 'GetSummary' , 'NRQL' ]
nrapi = 'https://api.newrelic.com/v2'
parser = argparse.ArgumentParser()
parser.add_argument("action")
args = parser.parse_args()
action=args.action

def GetSummary():
  result = requests.get("https://api.newrelic.com/v2/applications.json", headers={"Api-Key":nrkey})
  if result.status_code == 200:
    print(result.text)
  else:
    print("Error: {result.status_code}")
    print(result.request.headers)
    sys.exit(1)

eval(action+'()')
