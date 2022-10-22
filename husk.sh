#!/bin/sh

# assume using zsh for now...

item="$(tail -n 2 ~/.zsh_history | head -n 1)" # penultimate history item

sep=";"
case $item in
  *"${sep}"*)
    command=${item#*"${sep}"}
    comment="$*"
    new_zsh_history_line=": $(date +%s):0;${command} #HUSK# ${comment}"
    echo "${new_zsh_history_line}" >> ~/.zsh_history
    ;;
  *)
    exit
    ;;
esac


