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
    print('Siemens_interleaved_k')
elif site=='CMU':
    print('Siemens_interleaved_k')
elif site=='KKI':
    print('Philips_ASCEND_k')
elif site=='Leuven':
    print('Philips_ASCEND_k')
elif site=='MaxMun':
    print('Siemens_interleaved_k')
elif site=='NYU':
    print('Siemens_interleaved_k')
elif site=='OHSU':
    print('Siemens_interleaved_k')
elif site=='Olin':
    print('Siemens_ascending_k')
elif site=='Pitt':
    print('Siemens_interleaved_k')
elif site=='SBL':
    print('Philips_DESCEND_k')
elif site=='SDSU':
    print('none')
elif site=='Stanford':
    print('none')
elif site=='Trinity':
    print('Philips_ASCEND_k')
elif site=='UCLA':
    print('Siemens_interleaved_k')
elif site=='UM':
    print('GE_interleaved_k')
elif site=='USM':
    print('Siemens_interleaved_k')
elif site=='Yale':
    print('Siemens_interleaved_k')
else:
    raise Exception(f'Unknown ABIDE site {site} for subject {args.subject_label}')

