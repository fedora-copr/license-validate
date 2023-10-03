set -o pipefail
cd ~/projects/rhel/components/RHEL10/ && git pull --rebase
cd -
while read c; do 
        echo -n "$c,"
        grep "Default Assignee"  ~/projects/rhel/components/RHEL10/$c 2> /dev/null | cut -f 3 -d " " | tr '\n' ',' || echo -ne "Not in RHEL10,"
        grep "SST Pool"  ~/projects/rhel/components/RHEL10/$c 2> /dev/null | cut -f 3 -d " " | tr '\n' ',' || echo -n "Not in RHEL10,"
        grep "^$c$" eln-without-buildroot.txt 2> /dev/null >/dev/null && echo "" || echo "Buildroot only"
done < eln-not-migrated.txt > /tmp/a.csv
