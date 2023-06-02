set -o pipefail
while read c; do 
        echo -n "$c,"
        grep "Default Assignee"  ~/projects/rhel/components/RHEL10/$c 2> /dev/null | cut -f 3 -d " " | tr '\n' ',' || echo -ne "Not in RHEL10,"
        grep "SST Pool"  ~/projects/rhel/components/RHEL9/$c 2> /dev/null | cut -f 3 -d " " || echo "Not in RHEL9"
done < eln-not-migrated.txt > /tmp/a.csv
