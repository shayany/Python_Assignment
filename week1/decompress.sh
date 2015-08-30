if [ "$#" -eq "0" ]; then
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
		-h)
			echo "-d	directory	it gives a path to find all the files in it"
			shift; ;;
		-help)
			echo "-d	directory	it gives a path to find all the files in it"
			shift; ;;
		*)
			echo "Error:Invalid Argument"; exit ;;
	esac
done
list="$(find $d -name '*.gz')"
declare -i n
n=1
for file in $list
do
	echo "$n=$file"
	n=n+1
	gzip -d $file
done
