declare -i i
i=0
while [ $i -lt 1 ]
do
	echo $(date)
	trap ctrl_c SIGINT 
	function ctrl_c() 
	{
		clear
		echo $(date)
		echo "Bye bye"
		exit
	}	
done

