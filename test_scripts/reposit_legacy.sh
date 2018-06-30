# This runs an example repositorg command:
repositorg reposit-legacy --no-ask --letters 1 -p "nd750_" -e "NEF" "JPG" -d 4 "../../reposit_outdir_a/" "../example_data/source_a/"

# This checks that the output is actually correct:
if [ ! -f "../../reposit_outdir_a/a/nd750_a0018.JPG" ]; then
    exit 1
fi

if [ ! -f "../../reposit_outdir_a/a/nd750_a0018.NEF" ]; then
    echo "Lalal"
    exit 1
fi

if [ -f "../../reposit_outdir_a/a/nd750_a0019.JPG" ]; then
	exit 1
fi
