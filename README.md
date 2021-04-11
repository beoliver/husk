# husk

#### English

The outer covering of a grain or a seed.

- Synonyms: rind, shell, hull, covering

#### Norwegian

Imperative form of the the verb _huske_ - to remember or recollect

1.  [Initializing](#init)
2.  [Contexts](#context)
    1.  [init](#context_init)
    2.  [list](#context_show)
3.  [Tags](#tag)

    1. [add](#add_tag)
    2. [list](#show_tags)
    3. [clean](#clean_tags)

4.  [Bookmarks](#bookmarks)
    1. [add](#add_bookmark)
    1. [list](#find_bookmark)

# Initializing <a name="init"></a>

```sh
husk init <path>
```

Create a new `husk.db`

# Contexts <a name="context"></a>

## `ctx init` <a name="context_init"></a>

1. Create a `.husk_context` file in the indicated directory.
2. Adds context information to the `husk.db`

A context is a namespace.

By default the basepath of the current working directory is used as the `<name>` and the current working directory is used as the `<path>`.

```sh
husk ctx init [--name NAME] [--path PATH]
```

### Examples <a name="init_context_examples"></a>

The following examples assume that your current working directory is `/Users/yourname/Documents/foo`.

```
$ husk ctx init
This will perform the following action:
Initialize context 'foo' in directory '/Users/yourname/Documents/foo'
Proceed? [y/N]
```

```
$ husk ctx init --name bar
This will perform the following action:
Initialize context 'bar' in directory '/Users/yourname/Documents/foo'
Proceed? [y/N]
```

```
$ husk ctx init --path ~/Documents
This will perform the following action:
Initialize context 'foo' in directory '/Users/yourname/Documents'
Proceed? [y/N]
```

```
$ husk ctx init --name bar --path ~/Documents
This will perform the following action:
Initialize context 'bar' in directory '/Users/yourname/Documents'
Proceed? [y/N]
```

## `ctx list` <a name="context_show"></a>

Provides an overview of the different contexts that you have created.

```
husk ctx list [-p] [-c] [-A] [--in CONTEXT]
```

When called with no arguments the current working context is used as the default argument to `--in`.

| Flag   | Action                                                                      |
| ------ | --------------------------------------------------------------------------- |
| `-A`   | List **A**LL contexts. Equivalent to `husk ctx list -c --in <root-context>` |
| `-p`   | Include all **p**arent contexts                                             |
| `-c`   | Include all **c**hild contexts                                              |
| `--in` | Use a specified context                                                     |

### Examples <a name="init_context_examples"></a>

The following examples assume that your current working directory is `/Users/yourname/Documents/foo`.

```
$ husk ctx list
Context     Parent   Path
*foo        yourname /Users/yourname/Documents/foo
```

```
$ husk ctx list -p
Context     Parent   Path
yourname    -        /Users/yourname/
*foo        yourname /Users/yourname/Documents/foo
```

```
$ husk ctx list -c
Context     Parent   Path
*foo        yourname /Users/yourname/Documents/foo
foo-tasks   foo      /Users/yourname/Documents/foo/tasks
```

```
$ husk ctx list -pc
Context     Parent   Path
yourname    -        /Users/yourname/
*foo        yourname /Users/yourname/Documents/foo
foo-tasks   foo      /Users/yourname/Documents/foo/tasks
```

```
$ husk ctx list -A
Context     Parent   Path
yourname    -        /Users/yourname/
*foo        yourname /Users/yourname/Documents/foo
foo-tasks   foo      /Users/yourname/Documents/foo/tasks
bar         yourname /Users/yourname/Documents/bar
bar-ideas   bar      /Users/yourname/Documents/bar/ideas
```

```
$ husk ctx list -c --in bar
Context     Parent   Path
bar         yourname /Users/yourname/Documents/bar
bar-ideas   bar      /Users/yourname/Documents/bar/ideas
```

# Tags

## `tag add` <a name="add_tag"></a>

```
husk tag add NAME [-G] [--in CONTEXT]
```

| Flag   | Action                                                                        |
| ------ | ----------------------------------------------------------------------------- |
| `-G`   | Create a **G**lobal tag. Equivalent to `husk tag add TAG --in <root-context>` |
| `--in` | Create the tag in a specified context                                         |

## `tag list` <a name="show_tags"></a>

```
husk tag list [-p] [-c] [-A] [--in CONTEXT] [--pattern REGEX]
```

| Flag        | Action                                                                  |
| ----------- | ----------------------------------------------------------------------- |
| `-A`        | List **A**LL tags. Equivalent to `husk tag list -c --in <root-context>` |
| `-p`        | Include all tags defined within **p**arent contexts                     |
| `-c`        | Include all tags defined within **c**hild contexts                      |
| `--in`      | Use a specified context                                                 |
| `--pattern` | A regex pattern to marth against the tag                                |

### Examples <a name="tag_show"></a>

```
$ husk tag list -A
Tag     Context
tag1    foo
tag1    yourname
tag2    yourname
tag3    bar-ideas
```

Notice that the same tag may appear in different contexts.

## `tag clean` <a name="clean_tags"></a>

Removes any tags that are not used

```
husk tag clean [-p] [-c] [-A] [--in CONTEXT] [--dry-run]
```

| Flag        | Action                                                                    |
| ----------- | ------------------------------------------------------------------------- |
| `-A`        | Clean **A**LL tags. Equivalent to `husk tag clean -c --in <root-context>` |
| `-p`        | Include all tags defined within **p**arent contexts                       |
| `-c`        | Include all tags defined within **c**hild contexts                        |
| `--in`      | Use a specified context                                                   |
| `--dry-run` | Show which tags would be deleted                                          |

# Bookmarks <a name="bookmarks"></a>

Bookmarks are references to "external" documents.

## `bm add` <a name="add_bookmark"></a>

```
husk bm add PATH [-G] [--in CONTEXT] [--tags TAGS] [--note TEXT]
```

Where `PATH` is either a `URL` or a local file on disk.

| Flag     | Action                                                                                         |
| -------- | ---------------------------------------------------------------------------------------------- |
| `-G`     | Create a **G**lobal bookmark for the URL. Equivalent to `husk bm add PATH --in <root-context>` |
| `--in`   | Create the URL bookmark in a specified context                                                 |
| `--tag`  | Comma separated list of tags                                                                   |
| `--note` | An Optional description                                                                        |

When creating a bookmark, any tags supplied will be created within the desired context. This means that you can use the same value for a `tag` in multiple contexts.

## `bm list` <a name="show_bookmark"></a>

```
husk bm list [-A] [-p] [-c] [--in CONTEXT] [--tags TAGS] [--pattern REGEX]
```

| Flag        | Action                                                                          |
| ----------- | ------------------------------------------------------------------------------- |
| `-A`        | List all **A**ll bookmarks. Equivalent to `husk bm list -c --in <root-context>` |
| `-p`        | Include all bookmarks defined within **p**arent contexts                        |
| `-c`        | Include all bookmarks defined within **c**hild contexts                         |
| `--in`      | Create the URL bookmark in a specified context                                  |
| `--tag`     | Comma separated list of tags fo filter by                                       |
| `--pattern` | A regex pattern to marth against the link                                       |
