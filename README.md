# husk

#### English
The outer covering of a grain or a seed.
- Synonyms: rind, shell, hull, covering

#### Norwegian
Imperative form of the the verb _huske_ - to remember or recollect

```sh 
#!/bin/sh

# HUSK
HUSK_FILE="$HOME/.husk"
ARGS=$@

echo "\n#-HUSK-TIME-# $(date -u)" >> $HUSK_FILE
echo "#-HUSK-PLACE-# $(pwd)" >> $HUSK_FILE
echo "#-HUSK-COMMAND-# ${ARGS}" >> $HUSK_FILE
$SHELL -c "$ARGS" | tee -a $HUSK_FILE
```
