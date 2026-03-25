#formatted table to the terminal showing, per game, per user: number of wins, number of 
#losses, and Win/Loss ratio, sorted by one of these metrics.
#Usage: bash leaderboard.sh metric gameName
echo "hallo leaderboard.sh"

metric="$1"
gameName="$2"

if [[ "$metric" == "wins" ]]; then
	fieldnum=2
elif [[ "$metric" == "losses" ]]; then
	fieldnum=3
elif [[ "$metric" == "ratio" ]]; then
	fieldnum=4
fi

echo "Username,Wins,Losses,Win/Loss Ratio" > temp.csv
filename=".stats_${gameName}.csv"
touch filename
sort -t ',' -k${fieldnum} -n -r ${filename} >> temp.csv
cat temp.csv | column -t -s ',' 
rm temp.csv


