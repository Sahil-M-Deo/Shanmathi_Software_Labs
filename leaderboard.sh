#formatted table to the terminal showing, per game, per user: number of wins, number of 
#losses, and Win/Loss ratio, sorted by one of these metrics.
#Usage: bash leaderboard.sh metric gameName
echo "hallo leaderboard.sh"

metric="$1"
gameName="$2"

echo "Sorted by ${metric} for ${gameName} metric"
echo "Username,Wins,Losses,Win/Loss Ratio" > temp.csv
filename=".stats_${gameName}.csv"
touch ${filename} #create filename

if [[ "$metric" == "wins" ]]; then
	sort -n -t ',' -k2,2r -k3,3 ${filename} >> temp.csv
elif [[ "$metric" == "losses" ]]; then
	sort -n -t ',' -k3,3r -k2,2 ${filename} >> temp.csv
elif [[ "$metric" == "ratio" ]]; then
	sed 's/,inf$/,10000000000000/g' ${filename} | sort -n -t ',' -k4,4r -k2,2r | sed 's/,10000000000000$/,inf/g' >> temp.csv
fi

column -t -s ',' temp.csv
rm temp.csv


