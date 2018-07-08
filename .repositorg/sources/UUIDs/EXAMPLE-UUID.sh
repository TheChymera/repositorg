#!/usr/bin/env bash

# Specify the path of the data relative to the device root.
# This is left empty if the data is directly under the top level root of the device.
REL_PATH="transfer0/Chrisrtian/"

# Concatenate workflow here:
repositorg fetch --in-path "${REL_PATH}" "${1}" "${2}"
repositorg imgproc --unstack\
	--parameters "-auto-level -gravity Center -extent 2000x2000"\
	"/var/tmp/repositorg/${2}/"*TIF
repositorg reposit --no-ask\
	--in-regex '^(?P<subject>.+?)_(?P<slice>.+?)_(?P<zoom>[0-9]+?)x_w[1-9]'\
'*(?P<modality>.+?)( .*)?_scene(?P<scene>.+?)\.(?P<extension>.+?)$'\
	--out-string 'sub-{subject}/sub-{subject}_slice-{slice!l}_zoom-{zoom}_'\
'scene-{scene}_{modality!l}.{extension!l}'\
	"/var/tmp/repositorg/${2}/"\
	"~/histology/"

# You should really think about cleaning up, though ideally only after having tested the workflow.
rm -rf "/var/tmp/repositorg/${2}"
