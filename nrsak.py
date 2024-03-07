#!/usr/bin/env python3
import argparse
import re
import requests

parser = argparse.ArgumentParser()
parser.add_argument("a")
args = parser.parse_args()
print(args.a)
