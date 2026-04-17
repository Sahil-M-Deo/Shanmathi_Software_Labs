tab=$'\t'
endl=$'\n'
lock_time="60" #seconds
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
RESET="\e[0m"
GREY="\e[90m"

init_files(){
	touch ".users.tsv" ".failed_logins.csv"
}
handle_locked_users(){
	local username=$@
	local line=$(grep -E "^${username},[0-9]+$" .failed_logins.csv)
	local found_user=$?
	if ((found_user!=0))
	then 
		return 1
	fi

	local time_now=$(date +%s)
	local time_then=$(echo "$line" | cut -d ',' -f 2)
	if ((time_now-time_then>=lock_time))
	then 
		sed -i "/^$line$/d" .failed_logins.csv
		return 1
	else
		echo -e "${YELLOW}Please wait for $(( lock_time - (time_now - time_then) )) seconds before trying again${RESET}"
		return 0
	fi
}

username_exists(){
	local name="$@"
	grep -q "^${name}${tab}" .users.tsv
	return $?
}

hash(){
	echo -n "$@" | sha256sum | cut -d ' ' -f 1 #echo -n to avoid the trailing newline as it will change the hash
}

create_user(){
	echo "Username not found, creating new account:"
	local name="$@"
	local pwd
	read -r -s -p "Enter password: " pwd
	echo ""
	local hash_pwd=$(hash "$pwd")
	echo "${name}${tab}${hash_pwd}" >> .users.tsv
	echo -e "${endl}${GREEN}User '${name}' created successfully!${RESET}${endl}"
}

auth_user(){
	local line="$@"
	grep -Fxq "$line" .users.tsv
	return $?
}

is_valid_username(){
	[[ "$@" =~ ^[a-zA-Z0-9_]+$ ]]
	return $?
}

handle_three_attempts(){
	local attempts=3
	local username="$@"
	while ((attempts>0))
	do
		local pwd
	    read -r -s -p "Enter pwd: " pwd
		echo ""
	    local hash_pwd=$(hash "$pwd")
	    if auth_user "${username}${tab}${hash_pwd}"
		then
			echo -e "${GREEN}User ${username} Logged in successfully ${endl}${RESET}"
			break
		fi
		((attempts--))
		if ((attempts==0))
		then
			echo -e "${RED}Ok clearly you don't know the password... Locking account for $lock_time seconds${RESET}"
			echo "${username},$(date +%s)" >> .failed_logins.csv
			return 0
		else
			echo -e "${RED}wrong password, try again!${RESET}"
		fi
	done
	return 1
}


init_files

echo -e "${endl}${GREY}--User1 Login--${endl}${RESET}"
while true
do
    read -r -p "Enter username: " u1
	if ! is_valid_username "$u1"
	then
		echo -e "${RED}Invalid username. Only letters, numbers, and underscores are allowed.${RESET}"
		continue
	fi

	if username_exists "$u1"
	then
		handle_locked_users "$u1"  && continue
		handle_three_attempts "$u1" && continue
		break
	else
	    create_user "$u1"
		break
	fi
done

echo -e "${GREY}--User2 Login--${endl}${RESET}"
while true
do
    read -r -p "Enter username: " u2
	if [[ "$u2" == "$u1" ]]
	then
		echo -e "${RED}That's user1! Login as a different user bro${RESET}"
		continue
	fi

	if ! is_valid_username "$u2"
	then
		echo -e "${RED}Invalid username. Only letters, numbers, and underscores are allowed.${RESET}"
		continue
	fi

	if username_exists "$u2"
	then
		handle_locked_users "$u2" && continue
		handle_three_attempts "$u2" && continue
		break
	else
	    create_user "$u2"
		break
	fi
done

echo -e "${GREY}--LOGIN SUCCESSFUL--${endl}"
echo -e "Starting game...${RESET}"

python game.py "${u1}" "${u2}"