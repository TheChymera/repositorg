#!/usr/bin/env bash

# Specify the path of the data.
SOURCE_ID="transfer0/Chrisrtian/"

# Concatenate workflow here:
repositorg imgproc --unstack\
	--parameters "-auto-level -gravity Center -extent 2000x2000"\
	"/var/tmp/repositorg/${SOURCE_ID}/"*TIF
repositorg reposit --no-ask\
	--in-regex '^(?P<subject>.+?)_(?P<slice>.+?)_(?P<zoom>[0-9]+?)x_w[1-9]'\
'*(?P<modality>.+?)( .*)?_scene(?P<scene>.+?)\.(?P<extension>.+?)$'\
	--out-string 'sub-{subject}/sub-{subject}_slice-{slice!l}_zoom-{zoom}_'\
'scene-{scene}_{modality!l}.{extension!l}'\
	"/var/tmp/repositorg/${SOURCE_ID}/"\
	"~/histology/"

# You should really think about cleaning up, though ideally only after having tested the workflow.
rm -rf "/var/tmp/repositorg/${SOURCE_ID}"
