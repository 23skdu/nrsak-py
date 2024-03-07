#!/usr/bin/env python3
import sys, os, argparse, re, requests
try:
  nrkey = os.environ["NR_KEY"]
except:
  print('you must have NR_KEY environment variable set')
  sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument("a")
args = parser.parse_args()
print(args.a)
