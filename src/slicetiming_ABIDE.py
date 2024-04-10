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
elif site=='CMU':
    print(site)
elif site=='KKI':
    print(site)
elif site=='Leuven':
    print(site)
elif site=='MaxMun':
    print(site)
elif site=='NYU':
    print(site)
elif site=='OHSU':
    print(site)
elif site=='Olin':
    print(site)
elif site=='Pitt':
    print(site)
elif site=='SBL':
    print(site)
elif site=='SDSU':
    print(site)
elif site=='Stanford':
    print(site)
elif site=='Trinity':
    print(site)
elif site=='UCLA':
    print(site)
elif site=='UM':
    print(site)
elif site=='USM':
    print(site)
elif site=='Yale':
    print(site)
else:
    raise Exception(f'Unknown ABIDE site {site} for subject {args.subject_label}')



