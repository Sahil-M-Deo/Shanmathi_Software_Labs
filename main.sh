tab=$'\t'
endl=$'\n'
lock_time="60" #seconds
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
BLUE="\e[34m"
RESET="\e[0m"
BOLD="\e[1m"

recent_login(){
	username=$@
	line=$(grep -xE "^${username},[0-9]+$" failed_logins.csv)

	if [[ $? -ne 0 ]]
	then 
		return 1
	fi

	time_now=$(date +%s)
	time_then=$(echo "$line" | cut -d ',' -f 2)
	if (( time_now - time_then >= lock_time ))
	then 
		sed -i "/^$line$/d" failed_logins.csv
		return 1
	else
		echo -e "${YELLOW}Please wait for $(( lock_time - (time_now - time_then) )) seconds before trying again${RESET}"
		return 0
	fi
}

username_exists(){
	name="$@"
	while IFS=$'\t' read -r x y
	do
		if [[ "$x" == "$name" ]]
		then
			return 0
		fi
	done < users.tsv
	return 1
}

hash(){
	echo -n "$@" | sha256sum | cut -d ' ' -f 1 #echo -n to avoid the trailing newline as it will change the hash
}

create_user(){
	echo "Username not found, creating new account:"
	name="$@"
	read -s -p "Enter password: " pwd
	echo 
	hash_pwd=$(hash "$pwd")
	echo "${name}${tab}${hash_pwd}" >> users.tsv
}

auth_user(){
	line="$@"

	if grep -Fxq "$line" users.tsv
	then 
		return 0 
	fi
	return 1
}

is_valid_username(){
	username="$@"
	if [[ "$username" =~ ^[a-zA-Z0-9_]+$ ]]
	then
		return 0
	else
		echo -e "${RED}Invalid username. Only letters, numbers, and underscores are allowed.${RESET}"
		return 1
	fi
}

three_attempts(){
	attempts=3
	u1="$@"
	while (( attempts > 0 ))
	do
	    read -s -p "Enter pwd: " pwd
		echo
	    hash_pwd=$(hash "$pwd")
	    if auth_user "${u1}${tab}${hash_pwd}"
		then
			echo -e "${GREEN}User ${u1} Logged in successfully ${endl}${RESET}"
			break
		fi
		(( attempts-- ))
		if (( attempts == 0 ))
		then
			echo -e "${RED}Ok clearly you don't know the password... Locking account for $lock_time seconds${RESET}"
			echo "${u1},$(date +%s)" >> failed_logins.csv
			return 0
		else
			echo -e "${RED}wrong password, try again!${RESET}"
		fi
	done
	return 1
}

while true
do
    read -p "Enter username: " u1
	if ! is_valid_username "$u1"
	then
		continue
	fi

	if username_exists "$u1"
	then
		recent_login "$u1"  && continue
		three_attempts "$u1" && continue
		break
	else
	    create_user "$u1"
		break
	fi
done

while true
do
    read -p "Enter username: " u2
	if ! is_valid_username "$u2"
	then
		continue
	fi

	if username_exists "$u2"
	then
		recent_login "$u2" && continue
		three_attempts "$u2" && continue
		break
	else
	    create_user "$u2"
		break
	fi
done

python game.py "${u1}" "${u2}"
echo "hello welcome to games"