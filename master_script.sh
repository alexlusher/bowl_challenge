# This is a Master script, which processes all JSON files with campaign data

# create an array with all the filer/dir inside ~/myDir
arr=(data/*.json)
# iterate through array using a counter
for ((i=0; i<${#arr[@]}; i++)); do
    python campaign_loader.py -c ${arr[$i]}
    echo "...Processed ${arr[$i]}"
done
echo "Campaign data processing is complete"

