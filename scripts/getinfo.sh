#!/bin/bash


# parameter $1 = file with info

touch storage-unit.txt > storage-unit.txt #file for memory
#touch cpu-cache.txt #file for cpu
touch hw-info.txt > hw-info.txt #file for hardware devices
touch processes.txt > processes.txt #active processes
touch temp.txt > temp.txt #temperature
touch io.txt > io.txt #i/o devices

while read -r i; do
	acc=$(echo $i|awk '{print $1}')
	ip=$(echo $i|awk '{print $2}')
	echo "$acc's storage usage" >> storage-unit.txt 
	ssh $acc@$ip free -h >> storage-unit.txt
	echo "$acc's hw info:" >> hw-info.txt
	ssh $acc@$ip hwinfo --short >> hw-info.txt
	echo "$acc's active processes" >> processes.txt
	ssh $acc@$ip systemctl list-units --type=service --state=running >> processes.txt
	echo "$acc's temperature:" >> temp.txt 
	ssh $acc@$ip sensors >> temp.txt 
	echo "$acc's i/o devices:" >> io.txt 
	ssh $acc@$ip iostat >> io.txt 
done < $1
