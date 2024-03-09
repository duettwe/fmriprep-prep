#!/usr/bin/env python3

import argparse
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--jsonfile')
parser.add_argument('--polarity')
parser.add_argument('--intendedfor', nargs='*')
args = parser.parse_args()

with open(args.jsonfile) as f:
    jobj = json.loads(f.read())
    
    # Verify that this is a Philips scan before applying the Philips-
    # specific fixes for TotalReadoutTime and PhaseEncodingDirection
    if jobj['Manufacturer'] != 'Philips':
        raise Exception(f'Manufacturer is {jobj["Manufacturer"]} - expecting Philips')
    
    jobj['TotalReadoutTime'] = jobj['EstimatedTotalReadoutTime']

    if args.polarity=='+':
        jobj['PhaseEncodingDirection'] = jobj['PhaseEncodingAxis']
    elif args.polarity=='-':
        jobj['PhaseEncodingDirection'] = jobj['PhaseEncodingAxis'] + '-'
    else:
        raise Exception(f'Unknown polarity {args.polarity}')

    if args.intendedfor:
        jobj['IntendedFor'] = args.intendedfor
        
    print(json.dumps(jobj, indent = 4))
