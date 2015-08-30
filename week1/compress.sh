if [ "$#" -eq "0" ] || [ "$#" -eq "2" ] || [ "$#" -eq "3" ]; then
	echo "Error:Invalid Argument"
	exit
fi
while [ $# -gt 0 ]
do
	option=$1;
	shift;
	case "$option" in
		-d)
			d=$1
			shift; ;;
		-s)
			s=$1
			shift; ;;
		-h)
			echo "-d	directory	it gives a path to find all the files in it"
			echo "-s	size		minimum size for files"
			shift; ;;
		-help)
			echo "-d	directory	it gives a path to find all the files in it"
			echo "-s	size		minimum size for files"
			shift; ;;
		*)
			echo "Error:Invalid Argument"; exit ;;
	esac
done
list="$(find $d -type f -size $s)"
declare -i n
n=1
for file in $list
do
	echo "$n=$file"
	n=n+1
	gzip $file
done
