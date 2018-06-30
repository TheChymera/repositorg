# This runs an example repositorg command:
repositorg reposit --no-ask --in-regex '^(?P<subject>.+?)_(?P<slice>.+?)_(?P<zoom>[0-9]+?)x_w[1-9]*(?P<modality>.+?)( .*)?\.(?P<extension>.+?)$' --out-string 'sub-{subject}/sub-{subject}_slice-{slice!l}_zoom-{zoom}_{modality!l}.{extension!l}' ../example_data/source_b/ ../../reposit_outdir_b/

# This checks that the output is actually correct:
if [ ! -f "../../reposit_outdir_b/a/sub-5700/sub-5700_slice-a4_zoom-5_egfp.tif" ]; then
    exit 1
fi

if [ ! -f "../../reposit_outdir_b/a/sub-5700/sub-5700_slice-a4_zoom-5_dsred.tif" ]; then
    exit 1
fi

if [ -f "../../reposit_outdir_b/a/sub-5700/sub-5700_slice-a4_zoom-5_transmission.tif" ]; then
	exit 1
fi
