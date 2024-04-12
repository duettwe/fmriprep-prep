#!/usr/bin/env python3

import argparse
import json
import math
import nibabel
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--fmri_niigz')
parser.add_argument('--slicetiming')
args = parser.parse_args()


# Initialize empty json
json_data = {}

# Get some info from .nii.gz. Assume slice dim is dim[3] (k)
nii = nibabel.load(args.fmri_niigz)
nslices = nii.header['dim'][3]
tr = nii.header['pixdim'][4]

# fmriprep minimum needed fields
json_data['RepetitionTime'] = float(tr)

## Slice timing
# Assumes slices are evenly spaced in the TR (i.e. not a sparse
# acquisition, and any extra inter-TR delay is minimal)

if args.slicetiming:

    # Get a base list of ascending slice times that we will re-order
    basetimes = [x / nslices * tr for x in range(0,nslices)]

    # We can only handle certain specific cases
    if args.slicetiming in ['Philips_ASCEND_k', 'Siemens_ascending_k']:
        json_data['SliceEncodingDirection'] = 'k'
        json_data['SliceTiming'] = basetimes

    elif args.slicetiming in ['Philips_DESCEND_k', 'Siemens_descending_k']:
        json_data['SliceEncodingDirection'] = 'k'
        json_data['SliceTiming'] = list(reversed(basetimes))

    elif args.slicetiming in ['Siemens_interleaved_k']:
        json_data['SliceEncodingDirection'] = 'k'
        json_data['SliceTiming'] = [0 for x in basetimes]
        if nslices % 2 == 0:  # Even number of slices
            json_data['SliceTiming'][1::2] = basetimes[0:math.ceil(nslices/2)]
            json_data['SliceTiming'][0::2] = basetimes[math.ceil(nslices/2):]
        else: # Odd number of slices
            json_data['SliceTiming'][0::2] = basetimes[0:math.ceil(nslices/2)]
            json_data['SliceTiming'][1::2] = basetimes[math.ceil(nslices/2):]

    elif args.slicetiming in ['GE_interleaved_k']:
        json_data['SliceEncodingDirection'] = 'k'
        json_data['SliceTiming'] = [0 for x in basetimes]
        json_data['SliceTiming'][0::2] = basetimes[0:math.ceil(nslices/2)]
        json_data['SliceTiming'][1::2] = basetimes[math.ceil(nslices/2):]
        
    elif args.slicetiming in ['none']:
        pass

    else:
        raise Exception(f'Cannot handle slice timing of {args.slicetiming}')

## Print it out
print(json.dumps(json_data, indent = 4))
