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
    ordering = 'Siemens_interleaved_k'
elif site=='CMU':
    ordering = 'Siemens_interleaved_k'
elif site=='KKI':
    ordering = 'Philips_ASCEND_k'
elif site=='Leuven':
    ordering = 'Philips_ASCEND_k'
elif site=='MaxMun':
    ordering = 'Siemens_interleaved_k'
elif site=='NYU':
    ordering = 'Siemens_interleaved_k'
elif site=='OHSU':
    ordering = 'Siemens_interleaved_k'
elif site=='Olin':
    ordering = 'Siemens_ascending_k'
elif site=='Pitt':
    ordering = 'Siemens_interleaved_k'
elif site=='SBL':
    ordering = 'Philips_DESCEND_k'
elif site=='SDSU':
    ordering = 'none'
elif site=='Stanford':
    ordering = 'none'
elif site=='Trinity':
    ordering = 'Philips_ASCEND_k'
elif site=='UCLA':
    ordering = 'Siemens_interleaved_k'
elif site=='UM':
    ordering = 'GE_interleaved_k'
elif site=='USM':
    ordering = 'Siemens_interleaved_k'
elif site=='Yale':
    ordering = 'Siemens_interleaved_k'
else:
    raise Exception(f'Unknown ABIDE site {site} for subject {args.subject_label}')

print(ordering)

