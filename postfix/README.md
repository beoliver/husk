# Husk Postfix

```sh
$ cp husk.sh ~/bin/husk
$ chmod 755 ~/bin/husk
```

```sh
$ cat story.txt | rev | rev | husk
Sometimes you only realise
that you want to remember things
after the fact
```

```sh
$ cat ~/.husk/history
7b3371403274dfcbc6e14dbca27010ee10373ffea59735a0ddef0ebcb369d094 1601419924 cat story.txt | rev | rev
```

```sh
$ cat ~/.husk/out/7b3371403274dfcbc6e14dbca27010ee10373ffea59735a0ddef0ebcb369d094.txt
Sometimes you only realise
that you want to remember things
after the fact
```
