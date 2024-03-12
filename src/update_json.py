#!/usr/bin/env python3

import argparse
import json
import nibabel
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--fmri_niigz')
parser.add_argument('--polarity')
parser.add_argument('--intendedfor', nargs='*')
parser.add_argument('--slicetiming')
args = parser.parse_args()


jsonfile = args.fmri_niigz.replace('.nii.gz','.json')
with open(jsonfile) as f:
    jobj = json.loads(f.read())


## Phase encoding direction/info

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


## Slice timing

if args.slicetiming:

    # Get number of slices and TR from .nii.gz. Assume
    # slice axis is the third one.
    nii = nibabel.load(args.fmri_niigz)
    nslices = nii.header['dim'][3]
    tr = nii.header['pixdim'][4]

    # Check for existing
    if 'SliceTiming' in jobj:
        raise Exception(f'SliceTiming field exists in {jsonfile}')
    if 'SliceEncodingDirection' in jobj:
        raise Exception(f'SliceEncodingDirection field exists in {jsonfile}')

    # Get repetition time from .json to crosscheck
    tr2 = jobj['RepetitionTime']
    if abs(tr2-tr)>0.001:
        raise Exception(f'TR in {jsonfile} does not match {args.fmri_niigz}')

    # We can only handle certain specific cases
    #    Philips_ASCEND_k: ascending on third axis
    if args.slicetiming=='Philips_ASCEND_k':
        jobj['SliceEncodingDirection'] = 'k'
        jobj['SliceTiming'] = list(range(0,nslices) / nslices * tr)
    else:
        raise Exception(f'Cannot handle slice timing of {args.slicetiming}')


## Print it out
print(json.dumps(jobj, indent = 4))
