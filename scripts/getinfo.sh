#!/bin/bash


# parameter $1 = file with info
menu(){
	#echo "$1"
	PS3="Alege o optiune din meniu " 
	select ITEM in "Reseteaza fisier pentru capacitatea memoriei" "Reseteaza fisier despre dispozitive hardware" "Reseteaza fisier despre dispozitive I/O" "Reseteaza fisier despre procese active" "Reseteaza fisier despre temperatura" "Resetare fisier despre utilizatori si timpi de autentificare" "Exit" 
	do 
	    case $REPLY in 
		1) touch storage-unit.txt 
		truncate -s 0 storage-unit.txt #file for memory
		while IFS= read -r i; do
			acc=$(echo $i|awk '{print $1}')
			ip=$(echo $i|awk '{print $2}')
			echo "$acc's storage usage" >> storage-unit.txt 
			ssh $acc@$ip free -h >> storage-unit.txt
		done < $1
		echo "done"
		menu "$1"
		;; 
		
		2)touch hw-info.txt 
		truncate -s 0 hw-info.txt #file for hardware devices 
		while IFS= read -r i; do
			acc=$(echo $i|awk '{print $1}')
			ip=$(echo $i|awk '{print $2}')
			echo "$acc's hw info:" >> hw-info.txt
			ssh $acc@$ip hwinfo --short >> hw-info.txt
		done < $1
		menu "$1"
		;;
		 
		3)touch processes.txt 
		truncate -s 0 processes.txt #active processes
		while IFS= read -r i; do
			acc=$(echo $i|awk '{print $1}')
			ip=$(echo $i|awk '{print $2}')
			echo "$acc's active processes" >> processes.txt
			ssh $acc@$ip systemctl list-units --type=service --state=running >> processes.txt
		done < $1
		menu "$1"
		;;
		
		4)touch io.txt 
		truncate -s 0 io.txt #i/o devices
		while IFS= read -r i; do
			acc=$(echo $i|awk '{print $1}')
			ip=$(echo $i|awk '{print $2}')
			echo "$acc's i/o devices:" >> io.txt 
			ssh $acc@$ip iostat >> io.txt 
		done < $1 
		menu "$1"
		;;
		    
		5)touch temp.txt 
		truncate -s 0 temp.txt #temperature
		while IFS= read -r i; do
			acc=$(echo $i|awk '{print $1}')
			ip=$(echo $i|awk '{print $2}')
			echo "$acc's temperature:" >> temp.txt 
			ssh $acc@$ip sensors >> temp.txt
		done < $1 
		menu "$1"
		;;
		
		6)touch login.txt 
		truncate -s 0 login.txt 
		while IFS= read -r i; do
			acc=$(echo $i|awk '{print $1}')
			ip=$(echo $i|awk '{print $2}')
			echo "$acc's logins:" >> login.txt 
			ssh $acc@$ip last --since today >> login.txt
		done < $1 
		menu "$1"
		;; 
		  
		7) echo "Goodbye!" 
			exit
		;;
		
		*) echo "Optiune incorecta" 
			menu "$1"
	    esac
	done 
}

if [ $# -ne 1 ]; then
    echo "Usage: $0 <file_with_info>"
    exit 1
fi

menu "$1"
	
