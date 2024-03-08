#!/usr/bin/env python3

import argparse
import json
import string
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--jsonfile')
args = parser.parse_args()

validchars = string.ascii_letters + string.digits

def sanitize(input_string):
    output_string = ''
    for i in input_string:
        if i in validchars:
            output_string += i
        else:
            output_string += ''
    return output_string
    
with open(args.jsonfile) as f:
    jobj = json.loads(f.read())
    val = jobj['SeriesDescription']
    print(sanitize(val))
