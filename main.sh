tab=$'\t'
endl=$'\n'
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
	echo $@
}

create_user(){
	echo "Username not found, creating new account:"
	name="$@"
	read -p "Enter password: " pwd
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

three_attempts(){
	attempts=3
	u1="$@"
	while (( attempts > 0 ))
	do
	    read -p "Enter pwd: " pwd
	    hash_pwd=$(hash "$pwd")
	    if auth_user "${u1}${tab}${hash_pwd}"
		then
			echo "User ${u1} Logged in successfully ${endl}"
			break
		fi
		(( attempts-- ))
		if (( attempts == 0 ))
		then
			echo "Ok clearly you don't know the password... Terminating session immediately"
			exit 1
		else
			echo "wrong password, try again!"
		fi
	done
	
}

read -p "Enter username: " u1
if username_exists "$u1"
then
	three_attempts "$u1"
else
    create_user "$u1"
fi

read -p "Enter username: " u2
if username_exists "$u2"
then
	three_attempts "$u2"
else
    create_user "$u2"
fi

python3 game.py "${u1}" "${u2}"
echo "hello welcome to games"