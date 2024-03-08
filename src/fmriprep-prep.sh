#!/usr/bin/env bash
#
# Entrypoint for BIDS formatting

# Initialize default inputs
export t1_niigz=/INPUTS/t1.nii.gz
export fmri_niigzs=/INPUTS/fmri.nii.gz
export rpefwd_niigz=""
export rperev_niigz=""
export bids_dir=/INPUTS/BIDS
export sub=01
export ses=01

# Parse input options. Bit of extra gymnastics to allow multiple files
# for fMRIs. We will assume all .nii.gz have a matching .json sidecar
# in the same location with the same base filename.
t1_list=()
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in      
        --t1_niigz)       export t1_niigz="$2";       shift; shift ;;
        --rpefwd_niigz)   export rpefwd_niigz="$2";   shift; shift ;;
        --rperev_niigz)   export rperev_niigz="$2";   shift; shift ;;
        --bids_dir)       export bids_dir="$2";       shift; shift ;;
        --sub)            export sub="$2";            shift; shift ;;
        --ses)            export ses="$2";            shift; shift ;;
        --fmri_niigzs)
            next="$2"
            while ! [[ "$next" =~ -.* ]] && [[ $# > 1 ]]; do
                fmri_list+=("$next")
                shift
                next="$2"
            done
            shift ;;
        *) echo "Input ${1} not recognized"; shift ;;
    esac
done

# Count fmris
export num_fmris=${#fmri_list[@]}

# Show a bit of info
echo "Subject ${sub}, session ${ses}"
echo "fMRIs (${num_fmris}): ${fmri_list[@]}"
if [ -n "${rpefwd_niigz}" ]; then
    echo "RPE forward: ${rpefwd_niigz}"
    echo "RPE reverse: ${rperev_niigz}"
else
    echo "RPE images not specified"
fi

# Rename and relocate files according to bids func/fmap scheme
# https://bids-specification.readthedocs.io/en/stable/modality-specific-files/magnetic-resonance-imaging-data.html
# #case-4-multiple-phase-encoded-directions-pepolar

# We need to inject the PhaseEncodingDirection value for the +/- PE scans
# because Philips doesn't provide this in the dicoms and therefore dcm2niix
# doesn't either. We start with PhaseEncodingAxis and arbitrarily add
# a '-' on the scan that was labeled 'rev' above. This is done in update_json.py

# fMRIs
mkdir -p "${bids_dir}/sub-${sub}/ses-${ses}/func"
intended_tags=
for fmri_niigz in ${fmri_list[@]}; do
    
    fmri_json="${fmri_niigz%.nii.gz}.json"
    task=$(get_sanitized_series_description.py --jsonfile "${fmri_json}")
    run=$(get_run.py --jsonfile "${fmri_json}")
    
    intended_tag="ses-${ses}/func/sub-${sub}_ses-${ses}_task-${task}_run-${run}_bold"
    fmri_tag="sub-${sub}/${intended_tag}"

    cp "${fmri_niigz}" "${bids_dir}/${fmri_tag}.nii.gz"
    update_json.py --jsonfile ${fmri_json} --polarity + > "${bids_dir}/${fmri_tag}.json"

    intended_tags=(${intended_tags[@]} "${intended_tag}")

done

# TOPUP scans if they exist
if [ -n "${rpefwd_niigz}" ]; then

    mkdir -p "${bids_dir}/sub-${sub}/ses-${ses}/fmap"

    rpefwd_json="${rpefwd_niigz%.nii.gz}.json"
    rpefwd_tag="sub-${sub}/ses-${ses}/fmap/sub-${sub}_ses-${ses}_dir-fwd_epi"
    cp "${rpefwd_niigz}" "${bids_dir}/${rpefwd_tag}.nii.gz"
    update_json.py --jsonfile ${rpefwd_json} --polarity + --intendedfor ${intended_tags[@]} > "${bids_dir}/${rpefwd_tag}.json"

    rperev_json="${rperev_niigz%.nii.gz}.json"
    rperev_tag="sub-${sub}/ses-${ses}/fmap/sub-${sub}_ses-${ses}_dir-rev_epi"
    cp "${rperev_niigz}" "${bids_dir}/${rperev_tag}.nii.gz"
    update_json.py --jsonfile ${rperev_json} --polarity + --intendedfor ${intended_tags[@]} > "${bids_dir}/${rperev_tag}.json"

fi

# Finally, the required dataset description file
echo '{"Name": "Ready for fmriprep", "BIDSVersion": "1.0.2"}' > "${bids_dir}/dataset_description.json"

