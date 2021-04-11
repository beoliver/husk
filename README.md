# husk

#### English

The outer covering of a grain or a seed.

- Synonyms: rind, shell, hull, covering

#### Norwegian

Imperative form of the the verb _huske_ - to remember or recollect

1.  [Initializing](#init)
2.  [Contexts](#context)
    1.  [init](#context_init)
    2.  [info](#context_info)
    3.  [list](#context_show)
    4.  [set](#context_set)
    5.  [unset](#context_unset)
3.  [Tags](#tag)

    1. [add](#add_tag)
    2. [list](#show_tags)
    3. [clean](#clean_tags)

4.  [Bookmarks](#bookmarks)

    1. [add](#add_bookmark)
    1. [list](#find_bookmark)

5.  [Notes](#notes)
    1. [add](#add_bookmark)
    1. [list](#find_bookmark)

# Initializing <a name="init"></a>

```sh
husk init <path> [--with-context NAME]
```

| Flag             | Action                                 |
| ---------------- | -------------------------------------- |
| `--with-context` | Provide a custom **root context** name |

Create a new `~/.husk.db` and a `.husk` file in your home folder `~/`. If a custom `context` name is not passed then the default `<username>` is used.

Note that both `HUSK` is a reserved context name. You can use it as an argument to `--name` to specify the top level user filesystem context that is created when running then `init` command.

# Contexts <a name="context"></a>

Contexts are a fundamental abstraction used by `husk`.
A context (abbreviated to `ctx`) serves as a namespace that is used as an identifier whenever you `husk add` (remember!) something.

For example if you use your machine for both work and play you might find that you have two directories `~/Documents/work` and `~/Documents/play`.

If you are in the subdirectory `~/Documents/work/foo/src`, then you are in the **filesystem context** of `work`. Likewise, if you are in `~/Documents`, then you are **NOT** in the filesystem context of `work` nor `play`.

Yet, it is entirely reasonable for you to be thinking about `play` while in the `~/Documents/work` directory. Your **mental context** is `play` while your "physical" context is `work`.

This model has two outcomes.

1. A **filesystem context** can have at most one "parent" filesystem contexts.
2. A **filesystem context** can have one or more "child" filesystem contexts.

## `ctx init` <a name="context_init"></a>

The `ctx init` command is used to initiate a new context.

```sh
husk ctx init [--virtual] [--name NAME] [--path PATH]
```

| Flag        | Action                                                        |
| ----------- | ------------------------------------------------------------- |
| `--virtual` | Create a virtual context that is not tied to your filesystem. |
| `--name`    | Name of the context.                                          |
| `--path`    | Path to context root directory                                |

By default a **context** is mapped to your current working directory. For example if we were in `~/Documents/work` and run the following:

```
$ husk ctx init
```

Then two operations would be performed.

1. A `.husk` file is created in the current directory.
2. The context name and path information are added to the `husk.db`.

If we wanted to create a **virtual** context then we would use the following:

```
$ husk ctx init --virtual --name lol
```

In this case the following operation would be performed.

1. The context name is added to the `husk.db`.

## `ctx info` <a name="context_info"></a>

The `ctx info` command is provides information about the current context.

```sh
husk ctx info [-v] [-t] [--name CONTEXT]
```

| Flag     | Action                                    |
| -------- | ----------------------------------------- |
| `-v`     | Verbose                                   |
| `-t`     | Shorthand for `husk ctx info --name HUSK` |
| `--name` | Name of the context.                      |

If no `--name` is provided then `husk` will attempt to calculate your current **context**.

```
$ husk ctx info
```

If you want to find information about a virtual context that has not been [set](#context_set), then you must use the `--name` flag.

```
$ husk ctx info --name lol
```

## `ctx set` <a name="context_set"></a>

```
husk ctx set VIRUAL_CONTEXT
```

Set virual context for the entire filesystem. This means that `VIRUAL_CONTEXT` will used whenever a context is not **explicily** set using a command line flag.

## `ctx unset` <a name="context_unset"></a>

```
husk ctx unset
```

Unsets the virual context for the entire filesystem if active.

## `ctx list` <a name="context_show"></a>

Provides an overview of the different contexts that you have created.

```
husk ctx list [-p] [-c] [-A] [--name CONTEXT]
```

When called with no arguments the current working context or the current [set virtual context](#context_set) is used as the default argument to `--name`.

| Flag     | Action                                                                      |
| -------- | --------------------------------------------------------------------------- |
| `-A`     | List **A**LL contexts. Equivalent to `husk ctx list -c --in <root-context>` |
| `-p`     | Include all **p**arent contexts                                             |
| `-c`     | Include all **c**hild contexts                                              |
| `--name` | Use a specified context                                                     |

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
$ husk ctx list -c --name bar
Context     Parent   Path
bar         yourname /Users/yourname/Documents/bar
bar-ideas   bar      /Users/yourname/Documents/bar/ideas
```

# Tags

## `tag add` <a name="add_tag"></a>

```
husk tag add TAGS [-G] [--name CONTEXT]
```

Where `TAGS` is a comma separated list of tags

| Flag     | Action                                                                          |
| -------- | ------------------------------------------------------------------------------- |
| `-G`     | Create a **G**lobal tag. Equivalent to `husk tag add TAG --name <root-context>` |
| `--name` | Create the tag in a specified context                                           |

### Examples

Add a single tag `foo` to the current context.

```
$ husk tag add foo
```

Add the tags `foo`, `bar` and `baz` to the global context.

```
$ husk tag add -G foo,bar,baz
```

## `tag list` <a name="show_tags"></a>

```
husk tag list [-p] [-c] [-A] [--name CONTEXT] [--pattern REGEX]
```

| Flag        | Action                                                                    |
| ----------- | ------------------------------------------------------------------------- |
| `-A`        | List **A**LL tags. Equivalent to `husk tag list -c --name <root-context>` |
| `-p`        | Include all tags defined within **p**arent contexts                       |
| `-c`        | Include all tags defined within **c**hild contexts                        |
| `--name`    | Use a specified context                                                   |
| `--pattern` | A regex pattern to marth against the tag                                  |

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
husk tag clean [-p] [-c] [-A] [--name CONTEXT] [--dry-run]
```

| Flag        | Action                                                                      |
| ----------- | --------------------------------------------------------------------------- |
| `-A`        | Clean **A**LL tags. Equivalent to `husk tag clean -c --name <root-context>` |
| `-p`        | Include all tags defined within **p**arent contexts                         |
| `-c`        | Include all tags defined within **c**hild contexts                          |
| `--name`    | Use a specified context                                                     |
| `--dry-run` | Show which tags would be deleted                                            |

# Bookmarks <a name="bookmarks"></a>

Bookmarks are references to "external" documents.

## `bm add` <a name="add_bookmark"></a>

```
husk bm add PATH [-G] [--name CONTEXT] [--tags TAGS] [--meta TEXT]
```

Where `PATH` is either a `URL` or a local file on disk.

| Flag     | Action                                                                                           |
| -------- | ------------------------------------------------------------------------------------------------ |
| `-G`     | Create a **G**lobal bookmark for the URL. Equivalent to `husk bm add PATH --name <root-context>` |
| `--name` | Create the URL bookmark in a specified context                                                   |
| `--tag`  | Comma separated list of tags                                                                     |
| `--meta` | An Optional description                                                                          |

When creating a bookmark, any tags supplied will be created within the desired context. This means that you can use the same value for a `tag` in multiple contexts.

## `bm list` <a name="show_bookmark"></a>

```
husk bm list [-A] [-p] [-c] [--name CONTEXT] [--tags TAGS] [--pattern REGEX]
```

| Flag        | Action                                                                            |
| ----------- | --------------------------------------------------------------------------------- |
| `-A`        | List all **A**ll bookmarks. Equivalent to `husk bm list -c --name <root-context>` |
| `-p`        | Include all bookmarks defined within **p**arent contexts                          |
| `-c`        | Include all bookmarks defined within **c**hild contexts                           |
| `--name`    | Create the URL bookmark in a specified context                                    |
| `--tag`     | Comma separated list of tags fo filter by                                         |
| `--pattern` | A regex pattern to marth against the link                                         |

# Notes <a name="notes"></a>

Notes are blocks of text that you want to store

## `note add` <a name="add_note"></a>

```
husk note add [-G] [--name CONTEXT] [--tags TAGS]
```

Opens your default editor for the note
