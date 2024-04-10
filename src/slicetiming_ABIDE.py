#!/usr/bin/env python3
#
# Set site-specific slice timing code/tag for ABIDE data based on
# site prefix in subject label

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--subject_label', required=True)
args = parser.parse_args()

site = args.subject_label.split('_')[0]

if site=='Caltech':
    print(site)
elif site=='NYU':
    print(site)
else:
    raise Exception(f'Unknown ABIDE site {site} for subject {args.subject_label}')

