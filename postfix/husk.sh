#!/bin/sh

# uses ZSH history

# create a directory if needed
mkdir -p $HOME/.husk/out

# grab the last line of the zsh_history file
HISTORY_LINE=$(tail -1 ${HOME}/.zsh_history)

HISTORY_HUSK_SUFFIX=${HISTORY_LINE##*|}
HISTORY_NO_HUSK=$(echo ${HISTORY_LINE} | grep -o '^.*|' | sed -e 's/[[:space:]]*|[[:space:]]*$//')
TIMESTAMP=$(echo ${HISTORY_LINE} | cut -d ":" -f 2 | sed -e 's/^[[:space:]]*//')
COMMAND=${HISTORY_NO_HUSK#*;}
HISTORY_HASH=$(echo ${TIMESTAMP}${COMMAND} | shasum -a 256 | cut -d ' ' -f 1 )

# write the hash, date and command to the `history` file
echo "${HISTORY_HASH} ${TIMESTAMP} ${COMMAND}" >> $HOME/.husk/history 

# display output to user while writing to a file using the hash as the name
cat | while read data
do    
    echo "$data" | tee -a "$HOME/.husk/out/${HISTORY_HASH}.txt"
done

