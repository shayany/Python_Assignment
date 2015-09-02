if [ "$#" -eq "0" ] || [ "$#" -gt "2" ]; then
	echo "Error:Invalid Argument"
	exit
fi
if [ "$#" -eq "1" ]; then
	if ([ "$1" == "-h" ] || [ "$1" == "-help" ]); then
		echo "<directory>	<size>"
		echo "size should be a plain number"
		exit
	else
		echo "Error:Invalid Argument"
		exit
	fi
fi

if !([ -z $1 ] && [ -z $2 ]); then
	list="$(find $1 -type f -size +$2k)"
	declare -i n
	n=1
	for file in $list
	do
		echo "$n=$file"
		n=n+1
		gzip $file
	done
fi
