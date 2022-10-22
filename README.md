# husk

## What?
### Add a comment to your last command.

Updates your `~/.zsh_history` file to include the last command run with an appened comment.

### Example 
```sh
$ some-command --with -f -l ags
$ husk "some context about the command"
$ ls -la
$ history | tail -n 4
10136  some-command --with -f -l ags
10137  ./husk.sh "some context about the command"
10138* some-command --with -f -l ags #HUSK# some context about the command
10139  ls -la
```

## Why?

Because sometimes a command is _meaningful_, but not _memorable_. Being able to search for some additional text (keywords, tags, etc) makes findning the command in your history easier.

## Setup 
```sh
echo "alias husk=~HOME/path/to/husk.sh" >> ~/.zshrc
```
This menas that you can use `bck-i-search` to search for the comment that you left. the command can still be run. 

Can be combined with `fzf` - for example: 
```sh
history | fzf --height 40%
```

## Caveats

- Only support for `zsh`.
- Does not support multi line commands 