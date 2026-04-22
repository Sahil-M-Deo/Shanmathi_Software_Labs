#formatted table to the terminal showing, per game, per user: number of wins, number of 
#losses, and Win/Loss ratio, sorted by one of these metrics.
#Usage: bash leaderboard.sh metric gameName
clear
preprocess(){
	sed 's/,inf$/,1000000.000/' $@
}

postprocess(){
	awk '
	BEGIN{FS=","; OFS=",";}
	{
		if($4=="1000000.000")
		{
			$4="inf";
			print $0;
		}
		else
			printf "%s,%s,%s,%.3f\n",$1,$2,$3,$4;
	}
	'
}

metric="$1"
gameName="$2"

echo "Sorted by ${metric} for ${gameName}:"
echo
echo "Username,Wins,Losses,Win/Loss Ratio" > temp.csv
filename=".stats_${gameName}.csv"
touch ${filename} #create filename

if [[ "$metric" == "wins" ]]; then
	preprocess ${filename} | sort -t ',' -k2,2nr -k3,3n | postprocess >> temp.csv
elif [[ "$metric" == "losses" ]]; then
	preprocess ${filename} | sort -t ',' -k3,3nr -k2,2n | postprocess >> temp.csv
elif [[ "$metric" == "ratio" ]]; then
	preprocess ${filename} | sort -t ',' -k4,4nr -k2,2nr | postprocess >> temp.csv
fi

column -t -s ',' temp.csv

sort -t ',' -k2,2nr -k3,3n .user_total_wins.csv | head -5| sed 's/,/ /g' > .top5.txt

rm temp.csv


