# This runs an example repositorg command:
repositorg reposit --no-ask --letters 1 -p nd750_ -e NEF JPG -d 4 ../../reposit_outdir/ ../example_data/

# This checks that the output is actually correct:
if [ ! -f "../../reposit_outdir/a/nd750_a0018.JPG" ]; then
    exit 1
fi

if [ ! -f "../../reposit_outdir/a/nd750_a0018.NEF" ]; then
    echo "Lalal"
    exit 1
fi

if [ -f "../../reposit_outdir/a/nd750_a0019.JPG" ]; then
	exit 1
fi
