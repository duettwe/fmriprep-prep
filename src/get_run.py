#!/usr/bin/env python3

import argparse
import json
import string
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--jsonfile')
args = parser.parse_args()
    
with open(args.jsonfile) as f:
    jobj = json.loads(f.read())
    val = jobj['SeriesNumber']
    print(val)
