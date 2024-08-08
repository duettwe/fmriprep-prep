#!/usr/bin/env python3

import argparse
import json
import math
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
if not jobj['Manufacturer'].startswith('Philips'):
    raise Exception(f'Manufacturer is {jobj["Manufacturer"]} - expecting Philips')

if not 'TotalReadoutTime' in jobj:
    if 'EstimatedTotalReadoutTime' in jobj:
        jobj['TotalReadoutTime'] = jobj['EstimatedTotalReadoutTime']
    else:
        jobj['TotalReadoutTime'] = 0
        print('WARNING - no TotalReadoutTime or EstimatedTotalReadoutTime found - using 0')

if 'PhaseEncodingAxis' in jobj:
    if args.polarity=='+':
        jobj['PhaseEncodingDirection'] = jobj['PhaseEncodingAxis']
    elif args.polarity=='-':
        jobj['PhaseEncodingDirection'] = jobj['PhaseEncodingAxis'] + '-'
    else:
        raise Exception(f'Unknown polarity {args.polarity}')
else:
    print('WARNING - no PhaseEncodingAxis found - not updating PhaseEncodingDirection')


if args.intendedfor:
    jobj['IntendedFor'] = args.intendedfor


## Slice timing
# Assumes slices are evenly spaced in the TR (i.e. not a sparse
# acquisition, and any extra inter-TR delay is minimal)

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

    # Get a base list of ascending slice times that we will re-order
    basetimes = [x / nslices * tr for x in range(0,nslices)]

    # We can only handle certain specific cases
    if args.slicetiming in ['Philips_ASCEND_k', 'Siemens_ascending_k']:
        jobj['SliceEncodingDirection'] = 'k'
        jobj['SliceTiming'] = basetimes

    elif args.slicetiming in ['Philips_DESCEND_k', 'Siemens_descending_k']:
        jobj['SliceEncodingDirection'] = 'k'
        jobj['SliceTiming'] = list(reversed(basetimes))

    elif args.slicetiming in ['Siemens_interleaved_k']:
        jobj['SliceEncodingDirection'] = 'k'
        jobj['SliceTiming'] = [0 for x in basetimes]
        if nslices % 2 == 0:  # Even number of slices
            jobj['SliceTiming'][1::2] = basetimes[0:math.ceil(nslices/2)]
            jobj['SliceTiming'][0::2] = basetimes[math.ceil(nslices/2):]
        else: # Odd number of slices
            jobj['SliceTiming'][0::2] = basetimes[0:math.ceil(nslices/2)]
            jobj['SliceTiming'][1::2] = basetimes[math.ceil(nslices/2):]

    elif args.slicetiming in ['GE_interleaved_k']:
        jobj['SliceEncodingDirection'] = 'k'
        jobj['SliceTiming'] = [0 for x in basetimes]
        jobj['SliceTiming'][0::2] = basetimes[0:math.ceil(nslices/2)]
        jobj['SliceTiming'][1::2] = basetimes[math.ceil(nslices/2):]
        
    elif args.slicetiming in ['none']:
        pass

    else:
        raise Exception(f'Cannot handle slice timing of {args.slicetiming}')

## Print it out
print(json.dumps(jobj, indent = 4))
