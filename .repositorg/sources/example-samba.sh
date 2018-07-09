#!/usr/bin/env bash

# Add details about your SAMBA share:
IP="10.0.1.250"
SHARE="MyLab"
USER="myuser"
PASS="mypassword"
SOURCE="microscope02"
REMOTE_DATA_DIR="MyAccount/transit"

# Fetching is currently best handled explicitly for SAMBA
mkdir -p /tmp/repositorg/${SOURCE}
smbclient //${IP}/${SHARE} -U ${USER}%${PASS} -c 'lcd\
/tmp/repositorg/${SOURCE}; cd ${REMOTE_DATA_DIR}; prompt; mget *'

# Concatenate workflow here
repositorg imgproc --unstack\
	--parameters "-auto-level -gravity Center -extent 2000x2000"\
	"/var/tmp/repositorg/${SOURCE}/"*TIF
repositorg reposit\
  --in-regex '^(?P<subject>.+?)_(?P<slice>.+?)_(?P<zoom>[0-9]+?)x_w[1-9]\
*(?P<modality>.+?)( .*)?\.(?P<extension>.+?)$'\
  --out-string 'sub-{subject}/sub-{subject}_slice-{slice!l}_zoom-{zoom}_\
{modality!l}.{extension!l}'\
  "/tmp/repositorg/${SOURCE}" "/home/myuser/histology/"

# You should really think about cleaning up, though ideally only after having tested the workflow.
rm -rf "/var/tmp/repositorg/${SOURCE}"
