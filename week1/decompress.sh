if [ "$#" -eq "0" ] || [ "$#" -gt "1" ]; then
	echo "Error:Invalid Argument"
	exit
fi
if [ "$1" == "-help" ] ||  [ "$1" == "-h" ]; then
	echo "directory		it gives a path to find all the files in it"
	exit
fi

list="$(find $1 -name '*.gz')"
declare -i n
n=1
for file in $list
do
	echo "$n=$file"
	n=n+1
	gzip -d $file
done
